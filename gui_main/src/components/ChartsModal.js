import React from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';

const ModalOverlay = styled(motion.div)`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--bg-modal);
  backdrop-filter: blur(8px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-6);
`;

const ModalContainer = styled(motion.div)`
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-xl);
  width: 90vw;
  max-width: 1200px;
  height: 80vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: var(--shadow-xl);
`;

const ModalHeader = styled.div`
  padding: var(--spacing-6);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const ModalTitle = styled.h2`
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
`;

const CloseButton = styled(motion.button)`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  transition: all 0.2s ease;

  &:hover {
    background: var(--bg-primary);
    color: var(--text-primary);
  }
`;

const ModalContent = styled.div`
  flex: 1;
  padding: var(--spacing-6);
  overflow-y: auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-6);
  grid-template-rows: auto auto auto;
`;

const ChartSection = styled.div`
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-5);
  display: flex;
  flex-direction: column;
`;

const ChartTitle = styled.h3`
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-4) 0;
`;

const ChartContainer = styled.div`
  flex: 1;
  min-height: 200px;
  position: relative;
`;

const LineChart = styled.div`
  height: 100%;
  display: flex;
  align-items: end;
 gap:20px;
  padding: var(--spacing-4) 0;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: var(--border-color);
  }
`;

const LinePoint = styled(motion.div)`
  width: 8px;
  height: 8px;
  background: var(--primary-color);
  border-radius: 50%;
  position: relative;
  cursor: pointer;
  z-index: 2;

  &::before {
    content: '';
    position: absolute;
    bottom: 8px;
    left: 50%;
    transform: translateX(-50%);
    width: 2px;
    height: ${props => props.height}px;
    background: linear-gradient(180deg, var(--primary-color), transparent);
  }
`;

const DonutChart = styled.div`
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
`;

const DonutSvg = styled.svg`
  transform: rotate(-90deg);
`;

const DonutSegment = styled(motion.circle)`
  fill: none;
  stroke-width: 20;
  stroke: ${props => props.color};
  stroke-linecap: round;
  transform-origin: center;
`;

const DonutCenter = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
`;

const DonutValue = styled.div`
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--text-primary);
`;

const DonutLabel = styled.div`
  font-size: var(--font-size-sm);
  color: var(--text-muted);
`;

const BarChart = styled.div`
  height: 100%;
  display: flex;
  align-items: end;
  justify-content: space-around;
  gap: var(--spacing-2);
  padding: var(--spacing-4) 0;
`;

const Bar = styled(motion.div)`
  background: linear-gradient(180deg, var(--accent-color), var(--secondary-color));
  border-radius: var(--radius-sm);
  width: 30px;
  min-height: 10px;
  position: relative;
  cursor: pointer;

  &:hover {
    filter: brightness(1.1);
  }
`;

const BarLabel = styled.div`
  position: absolute;
  bottom: -24px;
  left: 50%;
  transform: translateX(-50%);
  font-size: var(--font-size-xs);
  color: var(--text-muted);
  white-space: nowrap;
`;

const HeatmapChart = styled.div`
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
  padding: var(--spacing-4);
`;

const HeatmapCell = styled(motion.div)`
  aspect-ratio: 1;
  border-radius: var(--radius-sm);
  background: ${props => {
    const intensity = props.value / 10;
    return `rgba(37, 99, 235, ${intensity})`;
  }};
  cursor: pointer;
  border: 1px solid var(--border-color);
  
  &:hover {
    border-color: var(--primary-color);
  }
`;

const LegendContainer = styled.div`
  display: flex;
  gap: var(--spacing-4);
  margin-top: var(--spacing-4);
  flex-wrap: wrap;
`;

const LegendItem = styled.div`
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
`;

const LegendColor = styled.div`
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: ${props => props.color};
`;

const LegendLabel = styled.span`
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
`;

const StatsGrid = styled.div`
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-4);
`;

const StatCard = styled(motion.div)`
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-4);
  text-align: center;
`;

const StatNumber = styled.div`
  font-size: var(--font-size-3xl);
  font-weight: 800;
  color: var(--primary-color);
  margin-bottom: var(--spacing-1);
`;

const StatLabel = styled.div`
  font-size: var(--font-size-sm);
  color: var(--text-muted);
  font-weight: 500;
`;

const ChartsModal = ({ isOpen, onClose }) => {
  const [barChartData, setBarChartData] = React.useState([]);
  const [lineChartData, setLineChartData] = React.useState([]);
  const [pieChartData, setPieChartData] = React.useState([]);
  React.useEffect(() => {
    fetch('http://127.0.0.1:8000/charts/bar')
    .then(response => (response.json()))
    .then(data => setBarChartData(data.chart))
    .catch(error => console.error('Error fetching bar chart data:', error));
    
    fetch('http://127.0.0.1:8000/charts/line')
    .then(response => (response.json()))
    .then(data => setLineChartData(data.chart))
    .catch(error => console.error('Error fetching line chart data:', error));

    fetch('http://127.0.0.1:8000/charts/pie')
    .then(response => (response.json()))  
    .then(data => setPieChartData(data.chart))
    .catch(error => console.error('Error fetching pie chart data:', error));


  }, [barChartData, lineChartData, pieChartData]);
  const equityTime = lineChartData;
  console.log("Line Chart Data:", equityTime);
  const assetsLiabilities = barChartData;
  console.log("Bar Chart Data:", assetsLiabilities);
  const assets = pieChartData;
  console.log("Pie Chart Data:", assets);

  // Generate heatmap data
  const heatmapData = Array.from({ length: 7 * 5 }, (_, i) => ({
    id: i,
    value: Math.floor(Math.random() * 10) + 1
  }));

  const circleRadius = 80;
  const circumference = 2 * Math.PI * circleRadius;

  return (
    <AnimatePresence>
      {isOpen && (
        <ModalOverlay
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
        >
          <ModalContainer
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            onClick={(e) => e.stopPropagation()}
          >
            <ModalHeader>
              <ModalTitle>Detailed Analytics</ModalTitle>
              <CloseButton
                onClick={onClose}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
              >
                ✕
              </CloseButton>
            </ModalHeader>

            <ModalContent>
              {/* Weekly Engagement Chart */}
              <ChartSection>
                <ChartTitle>Equity over time </ChartTitle>
                <ChartContainer>
                  <LineChart>
                    {equityTime.map((data) => (
                      <LinePoint
                        key={data.x}
                        height={Math.floor(data.y / 1000)}
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.1 }}
                        whileHover={{ scale: 1.5 }}
                      />
                    ))}
                  </LineChart>
                </ChartContainer>
              </ChartSection>

              {/* Sentiment Distribution */}
              <ChartSection>
                <ChartTitle>Sentiment Distribution</ChartTitle>
                <ChartContainer>
                  <DonutChart>
                    <DonutSvg width="200" height="200">
                      <DonutSegment
                        cx="100"
                        cy="100"
                        r={circleRadius}
                        color="var(--success-color)"
                        strokeDasharray={circumference}
                        strokeDashoffset={circumference * 0.32}
                        initial={{ strokeDashoffset: circumference }}
                        animate={{ strokeDashoffset: circumference * 0.32 }}
                        transition={{ duration: 1, delay: 0.3 }}
                      />
                      <DonutSegment
                        cx="100"
                        cy="100"
                        r={circleRadius}
                        color="var(--warning-color)"
                        strokeDasharray={circumference * 0.68}
                        strokeDashoffset={circumference * 0.85}
                        initial={{ strokeDashoffset: circumference }}
                        animate={{ strokeDashoffset: circumference * 0.85 }}
                        transition={{ duration: 1, delay: 0.6 }}
                      />
                    </DonutSvg>
                    <DonutCenter>
                      <DonutValue>68%</DonutValue>
                      <DonutLabel>Positive</DonutLabel>
                    </DonutCenter>
                  </DonutChart>
                  <LegendContainer>
                    <LegendItem>
                      <LegendColor color="var(--success-color)" />
                      <LegendLabel>Positive (68%)</LegendLabel>
                    </LegendItem>
                    <LegendItem>
                      <LegendColor color="var(--warning-color)" />
                      <LegendLabel>Neutral (22%)</LegendLabel>
                    </LegendItem>
                    <LegendItem>
                      <LegendColor color="var(--danger-color)" />
                      <LegendLabel>Negative (10%)</LegendLabel>
                    </LegendItem>
                  </LegendContainer>
                </ChartContainer>
              </ChartSection>

              {/* Assets vs Liabilities Distribution */}
              <ChartSection>
                <ChartTitle>Assets vs Liabilities</ChartTitle>
                <ChartContainer>
                  <BarChart>
                    {assetsLiabilities.map((data) => (
                      <Bar
                        key={data.x}
                        style={{ height: `${Math.floor(data.y/1000)}px` }}
                        initial={{ height: 0 }}
                        animate={{ height: `${Math.floor(data.y/1000)}px` }}
                        transition={{ delay: 0.1, duration: 0.6 }}
                        whileHover={{ scale: 1.1 }}
                      >
                        <BarLabel>{data.x}</BarLabel>
                      </Bar>
                    ))}
                  </BarChart>
                </ChartContainer>
              </ChartSection>

              {/* Activity Heatmap */}
              <ChartSection>
                <ChartTitle>Meeting Activity Heatmap</ChartTitle>
                <ChartContainer>
                  <HeatmapChart>
                    {heatmapData.map((cell, index) => (
                      <HeatmapCell
                        key={cell.id}
                        value={cell.value}
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: index * 0.01 }}
                        whileHover={{ scale: 1.1 }}
                      />
                    ))}
                  </HeatmapChart>
                </ChartContainer>
              </ChartSection>

              {/* Key Statistics */}
              <StatsGrid>
                <StatCard
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.2 }}
                  whileHover={{ scale: 1.05 }}
                >
                  <StatNumber>42m</StatNumber>
                  <StatLabel>Average Duration</StatLabel>
                </StatCard>

                <StatCard
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.3 }}
                  whileHover={{ scale: 1.05 }}
                >
                  <StatNumber>87%</StatNumber>
                  <StatLabel>Engagement Rate</StatLabel>
                </StatCard>

                <StatCard
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.4 }}
                  whileHover={{ scale: 1.05 }}
                >
                  <StatNumber>156</StatNumber>
                  <StatLabel>Action Items</StatLabel>
                </StatCard>

                <StatCard
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.5 }}
                  whileHover={{ scale: 1.05 }}
                >
                  <StatNumber>24</StatNumber>
                  <StatLabel>Topics Covered</StatLabel>
                </StatCard>
              </StatsGrid>
            </ModalContent>
          </ModalContainer>
        </ModalOverlay>
      )}
    </AnimatePresence>
  );
};

export default ChartsModal;
