let currentUser = null;
let isLoggedIn = false;
let hasClaimedReward = false;

async function login() {
    const usernameInput = document.getElementById('username').value;
    const passwordInput = document.getElementById('password').value;

    try {
        const response = await fetch('http://localhost:3000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: usernameInput, password: passwordInput }),
            credentials: 'include', // Include credentials for cookies to be sent with the request
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = { username: usernameInput };
            isLoggedIn = true;
            updateLoginStatus();
            showLoggedInContent();
        } else {
            alert(data.message || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
    }
}

async function logout() {
    try {
        const response = await fetch('http://localhost:3000/logout', {
            method: 'POST',
            credentials: 'include',
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = null;
            isLoggedIn = false;
            hasClaimedReward = false;
            updateLoginStatus();
            showLoggedOutContent();
        } else {
            alert(data.message || 'Logout failed');
        }
    } catch (error) {
        console.error('Logout error:', error);
    }
}

async function checkAuthentication() {
    try {
        const response = await fetch('http://localhost:3000/checkAuth', {
            method: 'GET',
            credentials: 'include',
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = { username: data.username };
            isLoggedIn = true;
            updateLoginStatus();
            showLoggedInContent();
        } else {
            currentUser = null;
            isLoggedIn = false;
            hasClaimedReward = false;
            updateLoginStatus();
            showLoggedOutContent();
        }
    } catch (error) {
        console.error('Authentication check error:', error);
    }
}

function updateLoginStatus() {
    const loginStatusElement = document.getElementById('loginStatus');

    if (isLoggedIn) {
        loginStatusElement.textContent = `Logged in as ${currentUser.username}`;
    } else {
        loginStatusElement.textContent = 'Not logged in';
    }
}

function showLoggedInContent() {
    const loginSection = document.getElementById('loginSection');
    loginSection.style.display = 'none';

    const rewardSection = document.getElementById('rewardSection');
    rewardSection.style.display = 'block';
}

function showLoggedOutContent() {
    const loginSection = document.getElementById('loginSection');
    loginSection.style.display = 'block';

    const rewardSection = document.getElementById('rewardSection');
    rewardSection.style.display = 'none';
}

async function claimReward() {
    if (isLoggedIn && !hasClaimedReward) {
        try {
            const response = await fetch('http://localhost:3000/claimReward', {
                method: 'POST',
                credentials: 'include',
            });

            const data = await response.json();

            if (response.ok) {
                document.getElementById('rewardMessage').textContent = 'Reward claimed!';
                hasClaimedReward = true;
            } else {
                alert(data.message || 'Failed to claim reward');
            }
        } catch (error) {
            console.error('Claim reward error:', error);
        }
    } else if (!isLoggedIn) {
        alert('You must be logged in to claim the reward');
    } else {
        alert('You have already claimed the reward for this week');
    }
}

// Add this line to check authentication on page load
checkAuthentication();
