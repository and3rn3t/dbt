#!/bin/bash
# 🚀 PRODUCTION DEPLOYMENT - QUICK START
# Copy and paste these commands on your Ubuntu server

echo "=========================================="
echo "🚀 dbt Analytics Production Deployment"
echo "=========================================="
echo ""
echo "Step 1: Clone the repository"
echo "----------------------------"
cat << 'EOF'
git clone https://github.com/and3rn3t/dbt.git
cd dbt
EOF

echo ""
echo "Step 2: Make deployment script executable"
echo "-----------------------------------------"
cat << 'EOF'
chmod +x deploy-production.sh
EOF

echo ""
echo "Step 3: Run the automated deployment"
echo "------------------------------------"
cat << 'EOF'
./deploy-production.sh
EOF

echo ""
echo "=========================================="
echo "That's it! The script will:"
echo "  ✅ Install Docker"
echo "  ✅ Configure firewall"
echo "  ✅ Set up environment"
echo "  ✅ Build images"
echo "  ✅ Start services"
echo "  ✅ Verify installation"
echo ""
echo "Total time: ~10-15 minutes"
echo "=========================================="
