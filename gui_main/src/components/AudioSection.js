import React, { useState, useEffect, useContext, useCallback } from "react";
import { RoomContext } from "@livekit/components-react";
import styled from "styled-components";
import {
  useVoiceAssistant,
  useTranscriptions,
  useParticipantInfo,
} from "@livekit/components-react";
import { motion } from "framer-motion";
import { Track } from "livekit-client";
import {
  useTracks,
  StartAudio,
  BarVisualizer,
} from "@livekit/components-react";

const AudioContainer = styled.div`
  background: var(--bg-card);
  padding: var(--spacing-6);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-6);
`;

const SectionHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const SectionTitle = styled.h2`
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
`;

const StatusBadge = styled.span`
  padding: var(--spacing-2) var(--spacing-3);
  background: ${(props) =>
    props.isRecording ? "rgba(239, 68, 68, 0.1)" : "rgba(107, 114, 128, 0.1)"};
  color: ${(props) =>
    props.isRecording ? "var(--danger-color)" : "var(--text-muted)"};
  border: 1px solid
    ${(props) =>
      props.isRecording
        ? "rgba(239, 68, 68, 0.2)"
        : "rgba(107, 114, 128, 0.2)"};
  border-radius: var(--radius-md);
  font-size: var(--font-size-xs);
  font-weight: 500;
`;

const AudioVisualization = styled.div`
  height: 120px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-4);
  position: relative;
  overflow: hidden;
`;

const WaveformContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  height: 100%;
`;

const WaveBar = styled(motion.div)`
  width: 4px;
  background: ${(props) =>
    props.isActive ? "var(--primary-color)" : "var(--border-color)"};
  border-radius: 2px;
  min-height: 8px;
`;

const AudioControls = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-4);
`;

const ControlButton = styled(motion.button)`
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: ${(props) => {
    if (props.variant === "record")
      return props.isActive ? "var(--danger-color)" : "rgba(239, 68, 68, 0.1)";
    if (props.variant === "primary") return "var(--primary-color)";
    return "var(--bg-tertiary)";
  }};
  color: ${(props) => {
    if (props.variant === "record")
      return props.isActive ? "white" : "var(--danger-color)";
    if (props.variant === "primary") return "white";
    return "var(--text-secondary)";
  }};
  border: 1px solid
    ${(props) => {
      if (props.variant === "record")
        return props.isActive
          ? "var(--danger-color)"
          : "rgba(239, 68, 68, 0.2)";
      if (props.variant === "primary") return "var(--primary-color)";
      return "var(--border-color)";
    }};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    transform: scale(1.05);
    box-shadow: var(--shadow-lg);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const AudioStats = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-4);
`;

const StatItem = styled.div`
  background: var(--bg-primary);
  padding: var(--spacing-4);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
`;

const StatLabel = styled.div`
  font-size: var(--font-size-xs);
  color: var(--text-muted);
  margin-bottom: var(--spacing-1);
`;

const StatValue = styled.div`
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
`;

const TranscriptionPanel = styled.div`
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-4);
  min-height: 120px;
`;

const TranscriptionHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: between;
  margin-bottom: var(--spacing-3);
`;

const TranscriptionTitle = styled.h3`
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--text-secondary);
  margin: 0;
`;

const TranscriptionText = styled.div`
  color: var(--text-primary);
  line-height: 1.6;
  font-size: var(--font-size-sm); -
  max-height: 80px;
  overflow-y: auto;
`;

const AudioSection = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [audio, setAudio] = useState(false);
  const { state, audioTrack } = useVoiceAssistant();
  const room = useContext(RoomContext);
  const roomParticipant = room.localParticipant;
  // Fetch a LiveKit token from the backend for this user and room
  // const fetchLiveKitToken = async () => {
  //   await fetch("http://127.0.0.1:5000/getToken")
  //     .then((Response) => Response.json())
  //     .then((data) => {
  //       setToken(data.token);
  //     })
  //     .catch((error) => {
  //       console.error("Error fetching LiveKit token:", error);
  //     });
  // };

  // useEffect(() => {
  //   const connectRoom = async () => {
  //     try {
  //       const livekitUrl = "wss://corelance-1egb2q0f.livekit.cloud";
  //       //

  //       await fetchLiveKitToken();
  //       const token1 =
  //         "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiYWthc2giLCJ2aWRlbyI6eyJyb29tSm9pbiI6dHJ1ZSwicm9vbSI6ImFrYXNoIiwiY2FuUHVibGlzaCI6dHJ1ZSwiY2FuU3Vic2NyaWJlIjp0cnVlLCJjYW5QdWJsaXNoRGF0YSI6dHJ1ZX0sInN1YiI6Im1heCIsImlzcyI6IkFQSWtheTJtanE4WEM3UCIsIm5iZiI6MTc2MTM5OTAyOCwiZXhwIjoxNzYxNDIwNjI4fQ.NM19-KRRiarcXGDzPHf6BidZ9Mk5PemE37KI-BX8LQ8";
  //       const roomInstance = new Room();
  //       await roomInstance.connect(livekitUrl, token1);
  //       setRoom(roomInstance);
  //     } catch (err) {
  //       console.error("LiveKit connection failed:", err);
  //     }
  //   };
  //   connectRoom();

  //   return () => {
  //     if (room) {
  //       room.disconnect();
  //     }
  //   };
  //   // eslint-disable-next-line
  // }, []);

  useEffect(() => {
    if (!room) {
      return;
    } else if (isRecording && room) {
      roomParticipant
        .setMicrophoneEnabled(true)
        .then(() => console.log("Microphone enabled"))
        .catch((e) => console.error("Mic error:", e));
    } else {
      roomParticipant.setMicrophoneEnabled(false);
    }
  }, [isRecording, room, roomParticipant]);
  var sid = !roomParticipant.getTrackPublication(Track.Source.Microphone)
    ? null
    : roomParticipant.getTrackPublication(Track.Source.Microphone).trackSid;
  const transcript = {
    participantIdentities: [useParticipantInfo().identity],
    trackSids: [sid],
  };
  const Transcription = () => {
    const transcriptions = useTranscriptions(transcript);
    return (
      <TranscriptionText>{transcriptions.map((t) => t.text)}</TranscriptionText>
    );
  };

  const toggleRecording = () => {
    setIsRecording((prev) => !prev);
  };

  const togglePlayback = () => {
    setIsPlaying((prev) => !prev);
  };

  const toggleAudio = () => {
    setAudio((prev) => !prev);
  };

  return (
    <AudioContainer>
      <SectionHeader>
        <SectionTitle>Audio Processing</SectionTitle>
        <StatusBadge isRecording={isRecording}>
          {isRecording ? "● Recording" : "Standby"}
        </StatusBadge>
      </SectionHeader>

      <AudioVisualization>
        <BarVisualizer trackRef={audioTrack} state={state} barCount={4} />
        
      </AudioVisualization>

      <AudioControls>
        <ControlButton
          variant="record"
          isActive={isRecording}
          onClick={() => {
            toggleRecording();
            toggleAudio();
          }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {isRecording ? "⏸" : "🎤"}
          {audio
            ? () => {
                roomParticipant.setMicrophoneEnabled(true);
                <StartAudio />;
                console.log("Track Unmuted");
              }
            : () => {
                roomParticipant.setMicrophoneEnabled(false);
                console.log("Track Muted");
              }}
        </ControlButton>

        <ControlButton
          variant="primary"
          onClick={togglePlayback}
          disabled={!isRecording}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {isPlaying ? "⏸" : "▶"}
        </ControlButton>

        <ControlButton whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
          ⏹
        </ControlButton>
      </AudioControls>

      <AudioStats>
        <StatItem>
          <StatLabel>Duration</StatLabel>
          <StatValue>{isRecording ? "00:45" : "00:00"}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Quality</StatLabel>
          <StatValue>HD</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Size</StatLabel>
          <StatValue>2.4 MB</StatValue>
        </StatItem>
      </AudioStats>

      <TranscriptionPanel>
        <TranscriptionHeader>
          <TranscriptionTitle>Live Transcription</TranscriptionTitle>
        </TranscriptionHeader>
        {isRecording ? (
          <Transcription />
        ) : (
          <TranscriptionText>
            <span style={{ color: "var(--text-muted)" }}>
              Start recording to see live transcription
            </span>
          </TranscriptionText>
        )}
      </TranscriptionPanel>
    </AudioContainer>
  );
};

export default AudioSection;
