#!/bin/bash
# Master Build Script for All Balrog Repositories
# Builds all Balrog repos as original ones

BALORG_SIGIL="[BALORG-MASTER]"
BUILD_ROOT="$(dirname "$0")/balrog_builds"

echo "=========================================="
echo "$BALORG_SIGIL Eco-Shell Balrog Build System"
echo "$BALORG_SIGIL Author: krustyspoofer-creator"
echo "=========================================="

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

build_repo() {
    local repo_name=$1
    local repo_path="$BUILD_ROOT/$repo_name"
    
    echo -e "\n${BLUE}$BALORG_SIGIL Building $repo_name...${NC}"
    
    if [ -f "$repo_path/build.sh" ]; then
        cd "$repo_path"
        chmod +x build.sh
        bash build.sh
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}$BALORG_SIGIL ✓ $repo_name built successfully${NC}"
        else
            echo -e "${RED}$BALORG_SIGIL ✗ $repo_name build failed${NC}"
            return 1
        fi
        cd - > /dev/null
    else
        echo -e "${RED}$BALORG_SIGIL ✗ Build script not found for $repo_name${NC}"
        return 1
    fi
}

# Build all Balorg repositories
echo -e "\n$BALORG_SIGIL Starting build process for all Balrog repositories..."

build_repo "super-ai"
build_repo "resources-monitoring"
build_repo "quantum-balorg"
build_repo "balorg-mine"
build_repo "cutting-edge-ai"

echo ""
echo "=========================================="
echo -e "${GREEN}$BALORG_SIGIL All Balrog builds complete!${NC}"
echo "=========================================="
echo ""
echo "$BALORG_SIGIL Built repositories:"
echo "  1. Super-AI (GridWorld AI)"
echo "  2. Resources Monitoring"
echo "  3. Quantum-Balorg (Quantum TLM)"
echo "  4. Balorg-mine"
echo "  5. Cutting-edge Balorg AI"
echo ""
echo "$BALORG_SIGIL Build location: $BUILD_ROOT"
echo ""
