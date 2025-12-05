/**
 * Utilitaires d'authentification côté client
 * Maison Manoé - Gestion des tokens JWT
 */

// Configuration
const AUTH_CONFIG = {
  TOKEN_KEY: "maison_manoe_token",
  TOKEN_TYPE_KEY: "maison_manoe_token_type",
  USER_KEY: "maison_manoe_user",
  API_BASE_URL: window.location.origin,
};

/**
 * Récupère le token d'authentification
 * @returns {string|null} Le token JWT ou null
 */
function getAuthToken() {
  return localStorage.getItem(AUTH_CONFIG.TOKEN_KEY) || sessionStorage.getItem(AUTH_CONFIG.TOKEN_KEY);
}

/**
 * Récupère le type de token
 * @returns {string|null} Le type de token (bearer) ou null
 */
function getTokenType() {
  return localStorage.getItem(AUTH_CONFIG.TOKEN_TYPE_KEY) || sessionStorage.getItem(AUTH_CONFIG.TOKEN_TYPE_KEY) || "bearer";
}

/**
 * Récupère les informations de l'utilisateur connecté
 * @returns {Object|null} Les données utilisateur ou null
 */
function getCurrentUser() {
  const userJson = localStorage.getItem(AUTH_CONFIG.USER_KEY) || sessionStorage.getItem(AUTH_CONFIG.USER_KEY);
  return userJson ? JSON.parse(userJson) : null;
}

/**
 * Vérifie si l'utilisateur est connecté
 * @returns {boolean} True si connecté, false sinon
 */
function isAuthenticated() {
  return !!getAuthToken();
}

/**
 * Stocke le token et les informations utilisateur
 * @param {string} token - Le token JWT
 * @param {Object} user - Les données utilisateur
 * @param {boolean} remember - Si true, utilise localStorage, sinon sessionStorage
 */
function setAuth(token, user, remember = false) {
  const storage = remember ? localStorage : sessionStorage;
  storage.setItem(AUTH_CONFIG.TOKEN_KEY, token);
  storage.setItem(AUTH_CONFIG.TOKEN_TYPE_KEY, "bearer");
  if (user) {
    storage.setItem(AUTH_CONFIG.USER_KEY, JSON.stringify(user));
  }
}

/**
 * Supprime le token et les informations utilisateur
 */
function clearAuth() {
  localStorage.removeItem(AUTH_CONFIG.TOKEN_KEY);
  localStorage.removeItem(AUTH_CONFIG.TOKEN_TYPE_KEY);
  localStorage.removeItem(AUTH_CONFIG.USER_KEY);
  sessionStorage.removeItem(AUTH_CONFIG.TOKEN_KEY);
  sessionStorage.removeItem(AUTH_CONFIG.TOKEN_TYPE_KEY);
  sessionStorage.removeItem(AUTH_CONFIG.USER_KEY);
}

/**
 * Déconnecte l'utilisateur et redirige vers la page de connexion
 * @param {string} returnUrl - URL de retour après connexion
 */
function logout(returnUrl = null) {
  clearAuth();
  const url = returnUrl ? `/connexion?return=${encodeURIComponent(returnUrl)}` : "/connexion";
  window.location.href = url;
}

/**
 * Effectue une requête API authentifiée
 * @param {string} endpoint - L'endpoint de l'API (ex: '/api/auth/me')
 * @param {Object} options - Options fetch (method, body, etc.)
 * @returns {Promise<Response>} La réponse de l'API
 */
async function authenticatedFetch(endpoint, options = {}) {
  const token = getAuthToken();

  if (!token) {
    throw new Error("Non authentifié");
  }

  const headers = {
    ...options.headers,
    Authorization: `Bearer ${token}`,
  };

  if (options.body && typeof options.body === "object") {
    headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(options.body);
  }

  const response = await fetch(`${AUTH_CONFIG.API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Si le token est expiré ou invalide
  if (response.status === 401) {
    clearAuth();
    window.location.href = `/connexion?return=${encodeURIComponent(window.location.pathname)}`;
    throw new Error("Token expiré");
  }

  return response;
}

/**
 * Récupère le profil de l'utilisateur connecté
 * @returns {Promise<Object>} Les données du profil
 */
async function fetchUserProfile() {
  const response = await authenticatedFetch("/api/auth/me");

  if (!response.ok) {
    throw new Error("Erreur lors de la récupération du profil");
  }

  const user = await response.json();

  // Mettre à jour le cache
  const storage = localStorage.getItem(AUTH_CONFIG.TOKEN_KEY) ? localStorage : sessionStorage;
  storage.setItem(AUTH_CONFIG.USER_KEY, JSON.stringify(user));

  return user;
}

/**
 * Protège une page en redirigeant si non authentifié
 * @param {string} loginUrl - URL de la page de connexion
 */
function requireAuth(loginUrl = "/connexion") {
  if (!isAuthenticated()) {
    window.location.href = `${loginUrl}?return=${encodeURIComponent(window.location.pathname)}`;
  }
}

/**
 * Met à jour l'interface utilisateur en fonction de l'état d'authentification
 * Affiche/masque les éléments avec data-auth-required ou data-auth-guest
 */
function updateAuthUI() {
  const isAuth = isAuthenticated();
  const user = getCurrentUser();

  // Éléments visibles seulement si connecté
  document.querySelectorAll("[data-auth-required]").forEach((el) => {
    el.style.display = isAuth ? "" : "none";
  });

  // Éléments visibles seulement si non connecté
  document.querySelectorAll("[data-auth-guest]").forEach((el) => {
    el.style.display = isAuth ? "none" : "";
  });

  // Afficher les informations utilisateur
  if (user) {
    document.querySelectorAll("[data-user-name]").forEach((el) => {
      el.textContent = `${user.first_name} ${user.last_name}`;
    });

    document.querySelectorAll("[data-user-email]").forEach((el) => {
      el.textContent = user.email;
    });

    document.querySelectorAll("[data-user-first-name]").forEach((el) => {
      el.textContent = user.first_name;
    });
  }
}

/**
 * Inscrit un nouvel utilisateur
 * @param {Object} userData - Les données d'inscription
 * @returns {Promise<Object>} Les données de l'utilisateur créé
 */
async function register(userData) {
  const response = await fetch(`${AUTH_CONFIG.API_BASE_URL}/api/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Erreur lors de l'inscription");
  }

  return await response.json();
}

/**
 * Connecte un utilisateur
 * @param {string} email - L'email de l'utilisateur
 * @param {string} password - Le mot de passe
 * @param {boolean} remember - Si true, garde la session active
 * @returns {Promise<Object>} Le token et les infos utilisateur
 */
async function login(email, password, remember = false) {
  // 1. Login
  const response = await fetch(`${AUTH_CONFIG.API_BASE_URL}/api/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Email ou mot de passe incorrect");
  }

  const tokenData = await response.json();

  // 2. Récupérer le profil
  const profileResponse = await fetch(`${AUTH_CONFIG.API_BASE_URL}/api/auth/me`, {
    headers: {
      Authorization: `Bearer ${tokenData.access_token}`,
    },
  });

  const user = profileResponse.ok ? await profileResponse.json() : null;

  // 3. Stocker les données
  setAuth(tokenData.access_token, user, remember);

  return { token: tokenData, user };
}

// Export pour utilisation globale
if (typeof window !== "undefined") {
  window.MaisonManoeAuth = {
    getAuthToken,
    getTokenType,
    getCurrentUser,
    isAuthenticated,
    setAuth,
    clearAuth,
    logout,
    authenticatedFetch,
    fetchUserProfile,
    requireAuth,
    updateAuthUI,
    register,
    login,
  };
}
