#!/bin/bash
# Production Deployment Script for Ubuntu Server
# Run this script on your Ubuntu server after cloning the repository

set -e  # Exit on error

echo "=========================================="
echo "🚀 dbt Analytics - Production Deployment"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo -e "${RED}❌ Please do not run as root. Run as regular user with sudo access.${NC}"
   exit 1
fi

echo -e "${YELLOW}Step 1: System Update${NC}"
echo "Updating system packages..."
sudo apt-get update -qq
sudo apt-get upgrade -y -qq
echo -e "${GREEN}✅ System updated${NC}"
echo ""

echo -e "${YELLOW}Step 2: Install Prerequisites${NC}"
echo "Installing required packages..."
sudo apt-get install -y -qq \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    make
echo -e "${GREEN}✅ Prerequisites installed${NC}"
echo ""

echo -e "${YELLOW}Step 3: Install Docker${NC}"
if command -v docker &> /dev/null; then
    echo "Docker already installed: $(docker --version)"
else
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    rm get-docker.sh
    
    # Add current user to docker group
    sudo usermod -aG docker $USER
    echo -e "${GREEN}✅ Docker installed${NC}"
    echo -e "${YELLOW}⚠️  You may need to log out and back in for docker group to take effect${NC}"
fi
echo ""

echo -e "${YELLOW}Step 4: Verify Docker${NC}"
if docker ps &> /dev/null; then
    echo -e "${GREEN}✅ Docker is working${NC}"
else
    echo -e "${YELLOW}⚠️  Applying docker group membership...${NC}"
    newgrp docker << END
    docker --version
END
fi
echo ""

echo -e "${YELLOW}Step 5: Check Project Directory${NC}"
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ docker-compose.yml not found!${NC}"
    echo "Please run this script from the dbt project directory"
    exit 1
fi
echo -e "${GREEN}✅ Project files found${NC}"
echo ""

echo -e "${YELLOW}Step 6: Configure Environment${NC}"
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo -e "${RED}⚠️  IMPORTANT: Edit .env file and change ALL passwords!${NC}"
    echo ""
    echo "Opening .env file for editing..."
    echo "Press any key when ready to edit..."
    read -n 1 -s
    nano .env
    echo -e "${GREEN}✅ .env configured${NC}"
else
    echo -e "${YELLOW}.env already exists. Review it? (y/n)${NC}"
    read -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        nano .env
    fi
fi
echo ""

# Secure .env file
chmod 600 .env
echo -e "${GREEN}✅ .env file secured (chmod 600)${NC}"
echo ""

echo -e "${YELLOW}Step 7: Configure Firewall${NC}"
if command -v ufw &> /dev/null; then
    echo "Configuring UFW firewall..."
    sudo ufw --force enable
    sudo ufw allow ssh
    sudo ufw allow 8888/tcp comment 'Jupyter Lab'
    sudo ufw allow 8080/tcp comment 'Adminer'
    sudo ufw status
    echo -e "${GREEN}✅ Firewall configured${NC}"
else
    echo "UFW not installed. Installing..."
    sudo apt-get install -y ufw
    sudo ufw --force enable
    sudo ufw allow ssh
    sudo ufw allow 8888/tcp
    sudo ufw allow 8080/tcp
    echo -e "${GREEN}✅ Firewall installed and configured${NC}"
fi
echo ""

echo -e "${YELLOW}Step 8: Build Docker Images${NC}"
echo "This may take 5-10 minutes..."
docker compose build
echo -e "${GREEN}✅ Docker images built${NC}"
echo ""

echo -e "${YELLOW}Step 9: Start Services${NC}"
docker compose up -d
echo "Waiting for services to start..."
sleep 10
echo -e "${GREEN}✅ Services started${NC}"
echo ""

echo -e "${YELLOW}Step 10: Check Service Status${NC}"
docker compose ps
echo ""

echo -e "${YELLOW}Step 11: Test dbt Connection${NC}"
echo "Testing database connection..."
if docker compose exec -T dbt dbt debug; then
    echo -e "${GREEN}✅ dbt connection successful!${NC}"
else
    echo -e "${RED}❌ dbt connection failed. Check logs with: docker compose logs dbt${NC}"
    exit 1
fi
echo ""

echo -e "${YELLOW}Step 12: Create Backup Directory${NC}"
mkdir -p ~/dbt/backups
chmod 755 ~/dbt/backups
echo -e "${GREEN}✅ Backup directory created${NC}"
echo ""

echo -e "${YELLOW}Step 13: Make Scripts Executable${NC}"
chmod +x backup-db.sh run-dbt.sh
echo -e "${GREEN}✅ Scripts made executable${NC}"
echo ""

echo "=========================================="
echo -e "${GREEN}✅ DEPLOYMENT COMPLETE!${NC}"
echo "=========================================="
echo ""
echo "🎉 Your dbt Analytics environment is running!"
echo ""
echo "Access your services:"
echo "  📊 Jupyter Lab: http://$(hostname -I | awk '{print $1}'):8888"
echo "  💾 Adminer:     http://$(hostname -I | awk '{print $1}'):8080"
echo ""
echo "Useful commands:"
echo "  docker compose ps              # Check status"
echo "  docker compose logs -f         # View logs"
echo "  docker compose exec dbt dbt run  # Run dbt models"
echo "  make help                      # See all make commands"
echo ""
echo "Next steps:"
echo "  1. Access Jupyter Lab and create your first notebook"
echo "  2. Load data into PostgreSQL"
echo "  3. Create dbt models"
echo "  4. Set up automated backups (see docs/DOCKER_DEPLOYMENT.md)"
echo ""
echo "Documentation: docs/DOCKER_DEPLOYMENT.md"
echo "Checklist: DEPLOYMENT_CHECKLIST.md"
echo ""
echo -e "${YELLOW}⚠️  Security Reminder:${NC}"
echo "  - Review and update passwords in .env"
echo "  - Set up SSL/TLS for production use"
echo "  - Configure regular backups"
echo "  - Review firewall rules"
echo ""
