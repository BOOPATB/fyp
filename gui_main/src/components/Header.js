import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const HeaderContainer = styled.header`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-6);
  height: 72px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
`;

const LogoSection = styled.div`
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
`;

const Logo = styled(motion.div)`
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 18px;
  cursor: pointer;
`;

const BrandName = styled.h1`
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
`;

const TagLine = styled.span`
  font-size: var(--font-size-sm);
  color: var(--text-muted);
  margin-left: var(--spacing-4);
`;

const Navigation = styled.nav`
  display: flex;
  align-items: center;
  gap: var(--spacing-6);
`;

const NavItem = styled(motion.button)`
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-secondary);
  font-weight: 500;
  font-size: var(--font-size-sm);
  transition: all 0.2s ease;
  
  &:hover {
    color: var(--text-primary);
    background: var(--bg-tertiary);
  }

  &.active {
    color: var(--primary-color);
    background: rgba(37, 99, 235, 0.1);
  }
`;

const StatusIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  padding: var(--spacing-2) var(--spacing-4);
  background: rgba(16, 185, 129, 0.1);
  border-radius: var(--radius-md);
  border: 1px solid rgba(16, 185, 129, 0.2);
`;

const StatusDot = styled.div`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--success-color);
  animation: pulse 2s ease-in-out infinite;
  
  @keyframes pulse {
    0%, 100% {
      opacity: 1;
      transform: scale(1);
    }
    50% {
      opacity: 0.7;
      transform: scale(1.1);
    }
  }
`;

const StatusText = styled.span`
  font-size: var(--font-size-xs);
  color: var(--success-color);
  font-weight: 500;
`;

const UserSection = styled.div`
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
`;

const UserAvatar = styled(motion.div)`
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: var(--font-size-sm);
  cursor: pointer;
  border: 2px solid var(--border-color);
`;

const Header = () => {
  return (
    <HeaderContainer>
      <LogoSection>
        <Logo
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          C
        </Logo>
        <div>
          <BrandName>Corelance</BrandName>
        </div>
        <TagLine>AI Meeting Assistant</TagLine>
      </LogoSection>

      <Navigation>
        <NavItem
          className="active"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          Dashboard
        </NavItem>
        <NavItem
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          Meetings
        </NavItem>
        <NavItem
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          Analytics
        </NavItem>
        <NavItem
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          Settings
        </NavItem>
      </Navigation>

      <UserSection>
        <StatusIndicator>
          <StatusDot />
          <StatusText>Live</StatusText>
        </StatusIndicator>
        
        <UserAvatar
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
        >
          HP
        </UserAvatar>
      </UserSection>
    </HeaderContainer>
  );
};

export default Header;
