import sqlite3
import pandas as pd
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HotelDatabase:
    def __init__(self, db_path: str = "hotel.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with tables and sample data"""
        logger.info("Initializing hotel database")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create rooms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number INTEGER UNIQUE NOT NULL,
                room_type TEXT NOT NULL,
                price_min REAL NOT NULL,
                price_max REAL NOT NULL,
                is_occupied BOOLEAN DEFAULT FALSE,
                guest_name TEXT,
                check_in_date TEXT,
                check_out_date TEXT,
                special_occasion TEXT,
                discount_percentage REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER,
                guest_name TEXT NOT NULL,
                check_in_date TEXT NOT NULL,
                check_out_date TEXT NOT NULL,
                total_amount REAL NOT NULL,
                discount_amount REAL DEFAULT 0,
                special_occasion TEXT,
                booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (room_id) REFERENCES rooms (room_id)
            )
        ''')
        
        # Insert sample room data if table is empty
        cursor.execute("SELECT COUNT(*) FROM rooms")
        if cursor.fetchone()[0] == 0:
            self._insert_sample_rooms(cursor)
        
        conn.commit()
        conn.close()
        logger.info("Database initialization completed")
    
    def _insert_sample_rooms(self, cursor):
        """Insert sample room data"""
        logger.info("Inserting sample room data")
        
        room_types = [
            ("Normal", 50, 80),
            ("Couple", 80, 120),
            ("2 Beds", 100, 150),
            ("4 Beds", 150, 200),
            ("Queen Size", 120, 180),
            ("Honeymoon", 200, 300),
            ("Deluxe Suite", 250, 400),
            ("Luxury", 350, 600)
        ]
        
        room_number = 101
        for room_type, min_price, max_price in room_types:
            for i in range(3):  # 3 rooms of each type
                cursor.execute('''
                    INSERT INTO rooms (room_number, room_type, price_min, price_max, is_occupied)
                    VALUES (?, ?, ?, ?, ?)
                ''', (room_number, room_type, min_price, max_price, False))
                room_number += 1
        
        logger.info(f"Inserted {len(room_types) * 3} sample rooms")
    
    def get_available_rooms_by_type(self, room_type: str) -> List[Dict]:
        """Get all available rooms of a specific type"""
        logger.info(f"Querying available {room_type} rooms")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT room_id, room_number, room_type, price_min, price_max
            FROM rooms 
            WHERE room_type = ? AND is_occupied = FALSE
        ''', (room_type,))
        
        rooms = []
        for row in cursor.fetchall():
            rooms.append({
                'room_id': row[0],
                'room_number': row[1],
                'room_type': row[2],
                'price_min': row[3],
                'price_max': row[4]
            })
        
        conn.close()
        logger.info(f"Found {len(rooms)} available {room_type} rooms")
        return rooms
    
    def get_all_room_types(self) -> List[Dict]:
        """Get all available room types with counts and price ranges"""
        logger.info("Querying all room types")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT room_type, 
                   COUNT(*) as total_rooms,
                   SUM(CASE WHEN is_occupied = FALSE THEN 1 ELSE 0 END) as available_rooms,
                   MIN(price_min) as min_price,
                   MAX(price_max) as max_price
            FROM rooms 
            GROUP BY room_type
        ''')
        
        room_types = []
        for row in cursor.fetchall():
            room_types.append({
                'room_type': row[0],
                'total_rooms': row[1],
                'available_rooms': row[2],
                'min_price': row[3],
                'max_price': row[4]
            })
        
        conn.close()
        logger.info(f"Found {len(room_types)} room types")
        return room_types
    
    def book_room(self, room_id: int, guest_name: str, check_in_date: str, 
                  check_out_date: str, special_occasion: str = None) -> Tuple[bool, str, float]:
        """Book a room and return success status, message, and final price"""
        logger.info(f"Attempting to book room {room_id} for {guest_name}")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if room is available
            cursor.execute('''
                SELECT room_type, price_min, price_max, is_occupied
                FROM rooms WHERE room_id = ?
            ''', (room_id,))
            
            room_data = cursor.fetchone()
            if not room_data:
                return False, "Room not found", 0
            
            room_type, price_min, price_max, is_occupied = room_data
            
            if is_occupied:
                return False, "Room is already occupied", 0
            
            # Calculate discount based on special occasion
            discount_percentage = self._calculate_discount(special_occasion)
            base_price = price_max  # Start with max price
            discount_amount = base_price * (discount_percentage / 100)
            final_price = base_price - discount_amount
            
            # Ensure final price is within bounds
            if final_price < price_min:
                final_price = price_min
                discount_amount = base_price - final_price
                discount_percentage = (discount_amount / base_price) * 100
            
            # Update room status
            cursor.execute('''
                UPDATE rooms 
                SET is_occupied = TRUE, 
                    guest_name = ?, 
                    check_in_date = ?, 
                    check_out_date = ?,
                    special_occasion = ?,
                    discount_percentage = ?
                WHERE room_id = ?
            ''', (guest_name, check_in_date, check_out_date, special_occasion, discount_percentage, room_id))
            
            # Create booking record
            cursor.execute('''
                INSERT INTO bookings (room_id, guest_name, check_in_date, check_out_date, 
                                    total_amount, discount_amount, special_occasion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (room_id, guest_name, check_in_date, check_out_date, final_price, discount_amount, special_occasion))
            
            conn.commit()
            logger.info(f"Successfully booked room {room_id} for {guest_name} at ${final_price:.2f}")
            
            return True, f"Room {room_id} booked successfully! Final price: ${final_price:.2f}", final_price
            
        except Exception as e:
            conn.rollback()
            logger.error(f"Error booking room: {str(e)}")
            return False, f"Error booking room: {str(e)}", 0
        finally:
            conn.close()
    
    def _calculate_discount(self, special_occasion: str) -> float:
        """Calculate discount percentage based on special occasion"""
        if not special_occasion:
            return 0
        
        occasion_lower = special_occasion.lower()
        if 'honeymoon' in occasion_lower:
            return 15.0
        elif 'birthday' in occasion_lower:
            return 10.0
        elif 'anniversary' in occasion_lower:
            return 12.0
        elif 'wedding' in occasion_lower:
            return 20.0
        elif 'special' in occasion_lower or 'celebration' in occasion_lower:
            return 8.0
        
        return 0
    
    def export_to_excel(self, filename: str = "hotel_bookings.xlsx"):
        """Export all booking data to Excel file"""
        logger.info(f"Exporting data to {filename}")
        conn = sqlite3.connect(self.db_path)
        
        # Export rooms data
        rooms_df = pd.read_sql_query('''
            SELECT room_number, room_type, price_min, price_max, is_occupied, 
                   guest_name, check_in_date, check_out_date, special_occasion, 
                   discount_percentage, created_at
            FROM rooms
        ''', conn)
        
        # Export bookings data
        bookings_df = pd.read_sql_query('''
            SELECT b.booking_id, r.room_number, b.guest_name, b.check_in_date, 
                   b.check_out_date, b.total_amount, b.discount_amount, 
                   b.special_occasion, b.booking_date
            FROM bookings b
            JOIN rooms r ON b.room_id = r.room_id
        ''', conn)
        
        conn.close()
        
        # Write to Excel with multiple sheets
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            rooms_df.to_excel(writer, sheet_name='Rooms', index=False)
            bookings_df.to_excel(writer, sheet_name='Bookings', index=False)
        
        logger.info(f"Data exported successfully to {filename}")
    
    def get_room_status(self, room_id: int) -> Optional[Dict]:
        """Get current status of a specific room"""
        logger.info(f"Querying status for room {room_id}")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT room_id, room_number, room_type, price_min, price_max, 
                   is_occupied, guest_name, check_in_date, check_out_date, 
                   special_occasion, discount_percentage
            FROM rooms WHERE room_id = ?
        ''', (room_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'room_id': row[0],
                'room_number': row[1],
                'room_type': row[2],
                'price_min': row[3],
                'price_max': row[4],
                'is_occupied': bool(row[5]),
                'guest_name': row[6],
                'check_in_date': row[7],
                'check_out_date': row[8],
                'special_occasion': row[9],
                'discount_percentage': row[10]
            }
        
        return None 
    

class MeetingDatabase:
    def __init__(self, db_path: str = "meeting.db"):
        self.db_path = db_path
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.init_database()

    def init_database(self):
        """Initialize the meeting database with table and sample data"""
        logger.info("Initializing meeting database")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create the meeting_files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meeting_files (
                file_id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL,
                embedding BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Insert sample meeting transcripts if table is empty
        cursor.execute("SELECT COUNT(*) FROM meeting_files")
        if cursor.fetchone()[0] == 0:
            self._insert_sample_meetings(cursor)

        conn.commit()
        conn.close()
        logger.info("Meeting database initialization completed")

    def _insert_sample_meetings(self, cursor):
        """Insert sample meeting transcripts with dummy embeddings"""
        logger.info("Inserting sample meeting transcripts")

        # For sample, we embed content now using the embedding model
        sample_meetings = [
            ("meeting_20250101.txt", "Discussed project timeline and deliverables."),
            ("meeting_20250215.txt", "Reviewed budget and resource allocation for Q2."),
            ("meeting_20250310.txt", "Analyzed customer feedback and upcoming product improvements."),
        ]

        for filename, content in sample_meetings:
            embedding = self.embedding_model.encode(content)
            embedding_blob = pickle.dumps(embedding)
            cursor.execute('''
                INSERT INTO meeting_files (filename, content, embedding)
                VALUES (?, ?, ?)
            ''', (filename, content, embedding_blob))

        logger.info(f"Inserted {len(sample_meetings)} sample meeting transcripts")

    def get_meeting_by_filename(self, filename: str) -> Optional[Dict]:
        """Retrieve a meeting transcript entry by filename"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT file_id, filename, content, embedding, created_at
            FROM meeting_files WHERE filename = ?
        ''', (filename,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "file_id": row[0],
                "filename": row[1],
                "content": row[2],
                "embedding": row[3],
                "created_at": row[4]
            }
        return None

    def list_all_meetings(self) -> List[Dict]:
        """Return all meeting transcript entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT file_id, filename, content, created_at
            FROM meeting_files ORDER BY created_at DESC
        ''')
        rows = cursor.fetchall()
        conn.close()

        meetings = []
        for row in rows:
            meetings.append({
                "file_id": row[0],
                "filename": row[1],
                "content": row[2],
                "created_at": row[3]
            })
        return meetings

    def add_file(self, filename: str, content: str) -> bool:
        """Add a meeting transcript file with embedding to database."""
        embedding = self.embedding_model.encode(content)
        embedding_blob = pickle.dumps(embedding)

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO meeting_files (filename, content, embedding) VALUES (?, ?, ?)",
                    (filename, content, embedding_blob)
                )
            logger.info(f"Added file '{filename}' successfully.")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"File '{filename}' already exists in database.")
            return False
        except Exception as e:
            logger.error(f"Error adding file '{filename}': {e}")
            return False

    def retrieve_file_content(self, filename: str) -> Optional[str]:
        """Retrieve the full content text of a meeting file by filename."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT content FROM meeting_files WHERE filename = ?", (filename,))
            row = cur.fetchone()
            if row:
                return row[0]
            else:
                logger.info(f"File '{filename}' not found.")
                return None

    def vector_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Perform a vector similarity search on meeting files for the query."""
        query_emb = self.embedding_model.encode(query)
        results = []

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT filename, content, embedding, created_at FROM meeting_files")
            for filename, content, embedding_blob, created_at in cursor.fetchall():
                embedding = pickle.loads(embedding_blob)
                similarity = np.dot(query_emb, embedding) / (np.linalg.norm(query_emb) * np.linalg.norm(embedding))
                results.append({
                    "filename": filename,
                    "content": content,
                    "similarity": similarity,
                    "created_at": created_at
                })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def truncate_files(self):
        """Delete all records from meeting_files table."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM meeting_files")
                conn.commit()
            logger.info("All meeting files truncated successfully.")
        except Exception as e:
            logger.error(f"Error truncating meeting files: {e}") 
