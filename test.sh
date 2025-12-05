#!/bin/bash

# Script de test pour Maison Manoé
# Teste tous les services et fonctionnalités principales

set -e  # Arrêt en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
BASE_URL="http://localhost:8000"
NEO4J_BOLT="bolt://localhost:7687"
NEO4J_HTTP="http://localhost:7474"
NPM_URL="http://localhost:81"

# Compteurs
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Fonction d'affichage
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_test() {
    echo -e "${YELLOW}🧪 Test: $1${NC}"
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Fonction de test HTTP
test_http() {
    local url=$1
    local description=$2
    local expected_code=${3:-200}
    
    print_test "$description"
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
    
    if [ "$response" = "$expected_code" ]; then
        print_success "$description - Code HTTP: $response"
        return 0
    else
        print_error "$description - Code HTTP attendu: $expected_code, reçu: $response"
        return 1
    fi
}

# Fonction de test JSON API
test_api_json() {
    local url=$1
    local description=$2
    
    print_test "$description"
    
    response=$(curl -s "$url" 2>/dev/null || echo "")
    
    if echo "$response" | python3 -m json.tool > /dev/null 2>&1; then
        print_success "$description - JSON valide"
        return 0
    else
        print_error "$description - JSON invalide ou réponse vide"
        return 1
    fi
}

# Fonction de test Docker
test_docker_container() {
    local container_name=$1
    local description=$2
    
    print_test "$description"
    
    if docker ps --format '{{.Names}}' | grep -q "^${container_name}$"; then
        status=$(docker inspect -f '{{.State.Status}}' "$container_name")
        if [ "$status" = "running" ]; then
            print_success "$description - Container en cours d'exécution"
            return 0
        else
            print_error "$description - Container existe mais statut: $status"
            return 1
        fi
    else
        print_error "$description - Container introuvable"
        return 1
    fi
}

# ============================================
# TESTS DOCKER
# ============================================
print_header "Tests des conteneurs Docker"

test_docker_container "maisonmanoe-neo4j" "Neo4j container"
test_docker_container "maisonmanoe-app" "Application container"
test_docker_container "nginx-proxy-manager" "Nginx Proxy Manager container"

# ============================================
# TESTS NEO4J
# ============================================
print_header "Tests Neo4j"

# Test interface web Neo4j
test_http "$NEO4J_HTTP" "Neo4j Browser (HTTP)"

# Test connexion Bolt (via Python)
print_test "Connexion Neo4j via Bolt"
if docker exec maisonmanoe-neo4j cypher-shell -u neo4j -p testpassword "RETURN 1" > /dev/null 2>&1; then
    print_success "Connexion Neo4j via Bolt"
else
    print_error "Connexion Neo4j via Bolt"
fi

# ============================================
# TESTS APPLICATION - PAGES PUBLIQUES
# ============================================
print_header "Tests des pages publiques"

test_http "$BASE_URL/" "Page d'accueil"
test_http "$BASE_URL/recherche" "Page de recherche"
test_http "$BASE_URL/panier" "Page panier"
test_http "$BASE_URL/favoris" "Page favoris"
test_http "$BASE_URL/connexion" "Page de connexion"
test_http "$BASE_URL/inscription" "Page d'inscription"
test_http "$BASE_URL/reset-password" "Page reset password"
test_http "$BASE_URL/a-propos" "Page à propos"
test_http "$BASE_URL/contact" "Page contact"
test_http "$BASE_URL/faq" "Page FAQ"
test_http "$BASE_URL/cgv" "Page CGV"
test_http "$BASE_URL/confidentialite" "Page confidentialité"
test_http "$BASE_URL/livraison" "Page livraison"
test_http "$BASE_URL/retours" "Page retours"

# ============================================
# TESTS APPLICATION - PAGES ADMIN
# ============================================
print_header "Tests des pages admin"

test_http "$BASE_URL/admin" "Dashboard admin"
test_http "$BASE_URL/admin/promos" "Page admin promotions"
test_http "$BASE_URL/admin/produits" "Page admin produits"
test_http "$BASE_URL/admin/texte" "Page admin texte"
test_http "$BASE_URL/admin/notifications" "Page admin notifications"

# ============================================
# TESTS API REST
# ============================================
print_header "Tests de l'API REST"

# Test API docs
test_http "$BASE_URL/docs" "Documentation API (Swagger)"
test_http "$BASE_URL/redoc" "Documentation API (ReDoc)"

# Test API produits
test_api_json "$BASE_URL/api/products" "API - Liste des produits"
test_api_json "$BASE_URL/api/products?limit=5" "API - Liste des produits (limit=5)"

# Test API healthcheck
print_test "API - Healthcheck"
health_response=$(curl -s "$BASE_URL/api/health" 2>/dev/null || echo "")
if echo "$health_response" | grep -q "status"; then
    print_success "API - Healthcheck"
else
    print_error "API - Healthcheck"
fi

# ============================================
# TESTS NGINX PROXY MANAGER
# ============================================
print_header "Tests Nginx Proxy Manager"

test_http "$NPM_URL" "NPM - Interface admin"

# ============================================
# TESTS FONCTIONNELS
# ============================================
print_header "Tests fonctionnels"

# Test inscription utilisateur
print_test "Inscription d'un utilisateur"
register_response=$(curl -s -X POST "$BASE_URL/api/auth/register" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "test_'$(date +%s)'@example.com",
        "password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User"
    }' 2>/dev/null || echo "")

if echo "$register_response" | grep -q "email"; then
    print_success "Inscription d'un utilisateur"
    
    # Extraire l'email pour le test de connexion
    TEST_EMAIL=$(echo "$register_response" | python3 -c "import sys, json; print(json.load(sys.stdin)['email'])" 2>/dev/null || echo "")
    
    # Test connexion
    if [ -n "$TEST_EMAIL" ]; then
        print_test "Connexion de l'utilisateur"
        login_response=$(curl -s -X POST "$BASE_URL/api/auth/login" \
            -H "Content-Type: application/json" \
            -d '{
                "email": "'"$TEST_EMAIL"'",
                "password": "TestPassword123!"
            }' 2>/dev/null || echo "")
        
        if echo "$login_response" | grep -q "access_token"; then
            print_success "Connexion de l'utilisateur"
            
            # Extraire le token
            ACCESS_TOKEN=$(echo "$login_response" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null || echo "")
            
            # Test route protégée
            if [ -n "$ACCESS_TOKEN" ]; then
                print_test "Accès route protégée avec token"
                me_response=$(curl -s -H "Authorization: Bearer $ACCESS_TOKEN" "$BASE_URL/api/auth/me" 2>/dev/null || echo "")
                
                if echo "$me_response" | grep -q "email"; then
                    print_success "Accès route protégée avec token"
                else
                    print_error "Accès route protégée avec token"
                fi
            fi
        else
            print_error "Connexion de l'utilisateur"
        fi
    fi
else
    print_error "Inscription d'un utilisateur"
fi

# ============================================
# TESTS DE PERFORMANCE
# ============================================
print_header "Tests de performance"

print_test "Temps de réponse de la page d'accueil"
response_time=$(curl -s -o /dev/null -w "%{time_total}" "$BASE_URL/" 2>/dev/null || echo "999")
response_time_ms=$(echo "$response_time * 1000" | bc 2>/dev/null || echo "999")

if (( $(echo "$response_time < 2" | bc -l) )); then
    print_success "Temps de réponse: ${response_time_ms}ms (< 2s)"
else
    print_error "Temps de réponse: ${response_time_ms}ms (> 2s)"
fi

# ============================================
# RÉSUMÉ DES TESTS
# ============================================
print_header "RÉSUMÉ DES TESTS"

echo -e "Tests totaux : ${BLUE}$TESTS_TOTAL${NC}"
echo -e "Tests réussis : ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests échoués : ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 Tous les tests sont passés avec succès !${NC}\n"
    exit 0
else
    echo -e "\n${RED}⚠️  $TESTS_FAILED test(s) ont échoué${NC}\n"
    exit 1
fi
