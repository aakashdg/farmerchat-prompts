#!/bin/bash

# Deployment script for farmerchat-prompts
# This script automates the process of building and publishing to PyPI

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== FarmerChat Prompts Deployment Script ===${NC}\n"

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo -e "${RED}Error: setup.py not found. Are you in the package root directory?${NC}"
    exit 1
fi

# Check for required tools
echo -e "${YELLOW}Checking for required tools...${NC}"
command -v python >/dev/null 2>&1 || { echo -e "${RED}Python is required but not installed.${NC}" >&2; exit 1; }
command -v pip >/dev/null 2>&1 || { echo -e "${RED}pip is required but not installed.${NC}" >&2; exit 1; }

# Install/upgrade build tools
echo -e "\n${YELLOW}Installing/upgrading build tools...${NC}"
pip install --upgrade pip build twine

# Run tests
echo -e "\n${YELLOW}Running tests...${NC}"
pip install -e .
python -m pytest tests/ -v
if [ $? -ne 0 ]; then
    echo -e "${RED}Tests failed! Please fix them before deploying.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ All tests passed!${NC}"

# Clean previous builds
echo -e "\n${YELLOW}Cleaning previous builds...${NC}"
rm -rf build/ dist/ *.egg-info
echo -e "${GREEN}✓ Cleaned${NC}"

# Build the package
echo -e "\n${YELLOW}Building the package...${NC}"
python -m build
echo -e "${GREEN}✓ Package built successfully${NC}"

# Check the build
echo -e "\n${YELLOW}Checking the build...${NC}"
twine check dist/*
if [ $? -ne 0 ]; then
    echo -e "${RED}Build check failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Build check passed${NC}"

# Ask what to do
echo -e "\n${YELLOW}What would you like to do?${NC}"
echo "1) Upload to TestPyPI (recommended for testing)"
echo "2) Upload to PyPI (production release)"
echo "3) Exit without uploading"
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo -e "\n${YELLOW}Uploading to TestPyPI...${NC}"
        echo "You'll need your TestPyPI token (https://test.pypi.org/manage/account/token/)"
        twine upload --repository testpypi dist/*
        
        if [ $? -eq 0 ]; then
            echo -e "\n${GREEN}✓ Successfully uploaded to TestPyPI!${NC}"
            echo -e "\nTest installation with:"
            echo -e "  pip install --index-url https://test.pypi.org/simple/ farmerchat-prompts"
        fi
        ;;
    2)
        echo -e "\n${YELLOW}Uploading to PyPI...${NC}"
        echo "You'll need your PyPI token (https://pypi.org/manage/account/token/)"
        
        read -p "Are you sure you want to upload to production PyPI? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            twine upload dist/*
            
            if [ $? -eq 0 ]; then
                echo -e "\n${GREEN}✓ Successfully uploaded to PyPI!${NC}"
                echo -e "\nInstall with:"
                echo -e "  pip install farmerchat-prompts"
                echo -e "\nPackage page:"
                echo -e "  https://pypi.org/project/farmerchat-prompts/"
            fi
        else
            echo -e "${YELLOW}Upload cancelled.${NC}"
        fi
        ;;
    3)
        echo -e "${YELLOW}Exiting without uploading.${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice.${NC}"
        exit 1
        ;;
esac

echo -e "\n${GREEN}=== Deployment Complete ===${NC}"
