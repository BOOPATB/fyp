
import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { GlobalStyles } from './styles/GlobalStyles';
import Header from './components/Header';
import AudioSection from './components/AudioSection';
import ChatSection from './components/ChatSection';
import AnalyticsSection from './components/AnalyticsSection';
import ChartsModal from './components/ChartsModal';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import {
 StartAudio,
  RoomAudioRenderer,
  
  RoomContext,

} from '@livekit/components-react';
import { Room, } from 'livekit-client';
import '@livekit/components-styles';


const serverUrl = 'wss://corelance-1egb2q0f.livekit.cloud';


const LoadingContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-size: 18px;
  color: var(--text-primary);
`;

const MainContainer = styled.main`
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
  padding: 0;
  margin: 0;
  overflow: hidden;
`;

const SectionsWrapper = styled.div`
  display: grid;
  grid-template-columns: 1.5fr 1.5fr 1fr; /* Audio bigger, Chat smaller, Analytics compact */
  gap: var(--spacing-4);
  padding: var(--spacing-4);
  width: 100%;
  box-sizing: border-box;
  height: 85vh; /* 🔥 ADD THIS - Fixed height */

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
    gap: var(--spacing-6);
    height: auto;
  }
`;
const AudioSectionWrapper = styled.div`
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  padding: var(--spacing-4);
  box-shadow: var(--shadow-md);
  height: 100%; /* 🔥 CHANGE from min-height to height */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
`;


// 💬 CHAT SECTION — Middle (scrollable + custom scrollbar)
const ChatSectionWrapper = styled.div`
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  height: 100%; /* 🔥 CHANGE from flex: 2 to height: 100% */
  overflow: hidden; /* 🔥 KEEP THIS */
`;


const AnalyticsSectionWrapper = styled.div`
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  padding: var(--spacing-3);
  box-shadow: var(--shadow-md);
  min-height: 85vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
`;



// function MyVideoConference({ room }) {
//   const tracks = useTracks(
//     [
//       { source: Track.Source.Camera, withPlaceholder: true },
//       { source: Track.Source.ScreenShare, withPlaceholder: false },
//     ],
//     { onlySubscribed: false }
//   );
//   return (
//     <GridLayout tracks={tracks} style={{ height: 'calc(100vh - var(--lk-control-bar-height))' }}>
//       <ParticipantTile />
//     </GridLayout>
//   );
// }

function App() {

  const [isChartsModalOpen, setIsChartsModalOpen] = useState(false);
  const [livekitToken, setLivekitToken] = useState(null);
  const [isLoadingToken, setIsLoadingToken] = useState(true);
  const [tokenError, setTokenError] = useState(null);

  const [room] = useState(() =>
    new Room({
      adaptiveStream: true,
      dynacast: true,
    })
  );

  // Fetch LiveKit token
  useEffect(() => {
    const fetchToken = async () => {
      try {
        const response = await fetch('http://localhost:5000/getToken');

        if (!response.ok) {
          throw new Error('Failed to fetch token from server');
        }

        const data = await response.json();
        setLivekitToken(data.token);
        console.log('LiveKit token fetched successfully');
      } catch (error) {
        console.error('Failed to fetch LiveKit token:', error);
        setTokenError(error.message);
      } finally {
        setIsLoadingToken(false);
      }
    };

    fetchToken();
  }, []);

  // Connect to LiveKit room 
  useEffect(() => {
    let mounted = true;

    const connect = async () => {
      if (mounted && livekitToken) {
        try {
          await room.connect(serverUrl, livekitToken);
          console.log('Connected to LiveKit room successfully');
        } catch (error) {
          console.error('Failed to connect to LiveKit:', error);
          setTokenError('Failed to connect to LiveKit room');
        }
      }
    };

    connect();

    return () => {
      mounted = false;
      room.disconnect();
      console.log('Disconnected from LiveKit room');
    };
  }, [room, livekitToken]);

  const openChartsModal = () => setIsChartsModalOpen(true);
  const closeChartsModal = () => setIsChartsModalOpen(false);

  // Show loading state while fetching token
  if (isLoadingToken) {
    return (
      <>
        <GlobalStyles />
        <LoadingContainer>
          <div>Loading LiveKit connection...</div>
        </LoadingContainer>
      </>
    );
  }

  // Show error if token fetch failed 
  if (tokenError) {
    console.warn('LiveKit connection error, but is the chat working tho:', tokenError);
  }

  return (
   <>
  <GlobalStyles />
  <div className="app">
    <Header />

    <MainContainer>
      {/* LiveKit video/audio conference section */}
      <RoomContext.Provider value={room}>
       
          {
            (() => {
              toast.error(`LiveKit Error: ${tokenError}\n Chat functionality will still work`, {
                position: "top-right",
                autoClose: 5000,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
              });

            }
          )}
          
              {/* <MyVideoConference room={room} /> */}
               <SectionsWrapper>
          <AudioSectionWrapper>
            <AudioSection />
          </AudioSectionWrapper>
  
          <ChatSectionWrapper>
            <ChatSection />
          </ChatSectionWrapper>
  
          <AnalyticsSectionWrapper>
            <AnalyticsSection onOpenCharts={openChartsModal} />
          </AnalyticsSectionWrapper>
        </SectionsWrapper>
         <ChartsModal isOpen={isChartsModalOpen} onClose={closeChartsModal} />
    <ToastContainer />

              <RoomAudioRenderer volume={1.0} muted={false} />
              {/* <ControlBar /> */}
      
    
       
        </RoomContext.Provider>
  
        {/* Dashboard sections arranged side by side */}
       
      </MainContainer>

   
  </div>
</>
  );
}
export default App;

