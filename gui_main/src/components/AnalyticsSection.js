import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const AnalyticsContainer = styled.div`
  background: var(--bg-card);
  padding: var(--spacing-6);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-6);
  overflow-y: auto;
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

const ViewChartsButton = styled(motion.button)`
  padding: var(--spacing-2) var(--spacing-4);
  background: var(--primary-color);
  color: white;
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  font-weight: 500;
  transition: all 0.2s ease;

  &:hover {
    background: var(--primary-hover);
  }
`;

const MetricsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-4);
`;

const MetricCard = styled(motion.div)`
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-4);
`;

const MetricLabel = styled.div`
  font-size: var(--font-size-xs);
  color: var(--text-muted);
  margin-bottom: var(--spacing-1);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const MetricValue = styled.div`
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-2);
`;

const MetricChange = styled.div`
  font-size: var(--font-size-xs);
  color: ${props => props.positive ? 'var(--success-color)' : 'var(--danger-color)'};
  display: flex;
  align-items: center;
  gap: var(--spacing-1);
`;

const AnalyticsChart = styled.div`
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-4);
  height: 200px;
  position: relative;
  display: flex;
  align-items: end;
  justify-content: space-around;
  gap: var(--spacing-2);
`;

const ChartBar = styled(motion.div)`
  background: linear-gradient(180deg, var(--primary-color), var(--accent-color));
  border-radius: var(--radius-sm);
  width: 20px;
  min-height: 10px;
  position: relative;
  cursor: pointer;

  &:hover {
    filter: brightness(1.1);
  }
`;

const ChartLabel = styled.div`
  position: absolute;
  bottom: -24px;
  left: 50%;
  transform: translateX(-50%);
  font-size: var(--font-size-xs);
  color: var(--text-muted);
  white-space: nowrap;
`;

const SentimentAnalysis = styled.div`
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-4);
`;

const SentimentTitle = styled.h3`
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-4) 0;
`;

const SentimentBar = styled.div`
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  height: 8px;
  position: relative;
  margin-bottom: var(--spacing-3);
  overflow: hidden;
`;

const SentimentFill = styled(motion.div)`
  height: 100%;
  border-radius: var(--radius-md);
  background: ${props => {
    if (props.sentiment === 'positive') return 'var(--success-color)';
    if (props.sentiment === 'negative') return 'var(--danger-color)';
    return 'var(--warning-color)';
  }};
`;

const SentimentLabels = styled.div`
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-xs);
  color: var(--text-muted);
`;

const TopicsSection = styled.div`
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-4);
`;

const TopicsTitle = styled.h3`
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-4) 0;
`;

const TopicsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: var(--spacing-3);
`;

const TopicItem = styled(motion.div)`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-3);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
`;

const TopicName = styled.span`
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  font-weight: 500;
`;

const TopicCount = styled.span`
  font-size: var(--font-size-xs);
  color: var(--text-muted);
  background: var(--bg-primary);
  padding: var(--spacing-1) var(--spacing-2);
  border-radius: var(--radius-sm);
`;

const ParticipantStats = styled.div`
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-4);
`;

const ParticipantTitle = styled.h3`
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-4) 0;
`;

const ParticipantList = styled.div`
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
`;

const ParticipantItem = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const ParticipantInfo = styled.div`
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
`;

const ParticipantAvatar = styled.div`
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--accent-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: white;
`;

const ParticipantName = styled.span`
  font-size: var(--font-size-sm);
  color: var(--text-primary);
`;

const ParticipantTime = styled.span`
  font-size: var(--font-size-xs);
  color: var(--text-muted);
`;

const AnalyticsSection = ({ onOpenCharts }) => {
  const chartData = [
    { day: 'Mon', value: 65 },
    { day: 'Tue', value: 45 },
    { day: 'Wed', value: 80 },
    { day: 'Thu', value: 55 },
    { day: 'Fri', value: 90 },
    { day: 'Sat', value: 40 },
    { day: 'Sun', value: 35 }
  ];

  const topics = [
    { name: 'Budget Planning', count: 12 },
    { name: 'Team Updates', count: 8 },
    { name: 'Product Launch', count: 6 },
    { name: 'Marketing Strategy', count: 4 }
  ];

  const participants = [
    { name: 'John Smith', time: '15m 30s', avatar: 'JS' },
    { name: 'Sarah Wilson', time: '12m 45s', avatar: 'SW' },
    { name: 'Mike Johnson', time: '8m 20s', avatar: 'MJ' },
    { name: 'Lisa Chen', time: '6m 15s', avatar: 'LC' }
  ];

  return (
    <AnalyticsContainer>
      <SectionHeader>
        <SectionTitle>Meeting Analytics</SectionTitle>
        <ViewChartsButton
          onClick={onOpenCharts}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          View Charts
        </ViewChartsButton>
      </SectionHeader>

      <MetricsGrid>
        <MetricCard
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <MetricLabel>Total Duration</MetricLabel>
          <MetricValue>42m 15s</MetricValue>
          <MetricChange positive>
            ↑ 12% vs last meeting
          </MetricChange>
        </MetricCard>

        <MetricCard
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <MetricLabel>Participants</MetricLabel>
          <MetricValue>8</MetricValue>
          <MetricChange positive>
            ↑ 2 more than planned
          </MetricChange>
        </MetricCard>

        <MetricCard
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <MetricLabel>Action Items</MetricLabel>
          <MetricValue>15</MetricValue>
          <MetricChange>
            → Same as last week
          </MetricChange>
        </MetricCard>

        <MetricCard
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <MetricLabel>Engagement</MetricLabel>
          <MetricValue>87%</MetricValue>
          <MetricChange positive>
            ↑ 5% improvement
          </MetricChange>
        </MetricCard>
      </MetricsGrid>

      <AnalyticsChart>
        {chartData.map((data, index) => (
          <ChartBar
            key={data.day}
            style={{ height: `${data.value}%` }}
            initial={{ height: 0 }}
            animate={{ height: `${data.value}%` }}
            transition={{ delay: index * 0.1, duration: 0.6 }}
            whileHover={{ scale: 1.05 }}
          >
            <ChartLabel>{data.day}</ChartLabel>
          </ChartBar>
        ))}
      </AnalyticsChart>

      <SentimentAnalysis>
        <SentimentTitle>Overall Sentiment</SentimentTitle>
        <SentimentBar>
          <SentimentFill
            sentiment="positive"
            initial={{ width: 0 }}
            animate={{ width: '68%' }}
            transition={{ duration: 1, delay: 0.5 }}
          />
        </SentimentBar>
        <SentimentLabels>
          <span>Negative</span>
          <span>Neutral</span>
          <span>Positive (68%)</span>
        </SentimentLabels>
      </SentimentAnalysis>

      <TopicsSection>
        <TopicsTitle>Key Topics Discussed</TopicsTitle>
        <TopicsList>
          {topics.map((topic, index) => (
            <TopicItem
              key={topic.name}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.02 }}
            >
              <TopicName>{topic.name}</TopicName>
              <TopicCount>{topic.count} mentions</TopicCount>
            </TopicItem>
          ))}
        </TopicsList>
      </TopicsSection>

      <ParticipantStats>
        <ParticipantTitle>Speaking Time</ParticipantTitle>
        <ParticipantList>
          {participants.map((participant, index) => (
            <ParticipantItem key={participant.name}>
              <ParticipantInfo>
                <ParticipantAvatar>{participant.avatar}</ParticipantAvatar>
                <ParticipantName>{participant.name}</ParticipantName>
              </ParticipantInfo>
              <ParticipantTime>{participant.time}</ParticipantTime>
            </ParticipantItem>
          ))}
        </ParticipantList>
      </ParticipantStats>
    </AnalyticsContainer>
  );
};

export default AnalyticsSection;
