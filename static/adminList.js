document.addEventListener('DOMContentLoaded', () => {
    const editUserModal = document.getElementById('editUserModal');
    const editUserForm = document.getElementById('editUserForm');

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Edit User
    document.addEventListener('click', async (e) => {
        if (e.target.classList.contains('edit-user')) {
            e.preventDefault();
            const userId = e.target.dataset.id;
            
            try {
                const response = await fetch(`/api/users/${userId}/`);
                const user = await response.json();
                
                // Fill the form with user data
                document.getElementById('username').value = user.username;
                document.getElementById('email').value = user.email;
                document.getElementById('is_active').value = user.is_active.toString();
                
                // Show the modal
                editUserModal.style.display = 'block';
                
                // Update form submission handler for editing
                editUserForm.onsubmit = async (e) => {
                    e.preventDefault();
                    const formData = new FormData(editUserForm);
                    const csrftoken = getCookie('csrftoken');

                    try {
                        const response = await fetch(`/api/users/${userId}/`, {
                            method: 'PUT',
                            headers: {
                                'X-CSRFToken': csrftoken,
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                username: formData.get('username'),
                                email: formData.get('email'),
                                is_active: formData.get('is_active') === 'true'
                            })
                        });

                        if (response.ok) {
                            const updatedUser = await response.json();
                            updateUserInPage(userId, updatedUser);
                            editUserModal.style.display = 'none';
                            editUserForm.reset();
                        } else {
                            console.error('Error updating user');
                        }
                    } catch (error) {
                        console.error('Error:', error);
                    }
                };
            } catch (error) {
                console.error('Error:', error);
            }
        }
    });

    // Toggle User Status
    document.addEventListener('click', async (e) => {
        if (e.target.classList.contains('toggle-status')) {
            e.preventDefault();
            const userId = e.target.dataset.id;
            const csrftoken = getCookie('csrftoken');
            const currentStatus = e.target.textContent.trim() === 'Деактивировать';

            try {
                const response = await fetch(`/api/users/${userId}/toggle_status/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        is_active: !currentStatus
                    })
                });

                if (response.ok) {
                    const user = await response.json();
                    updateUserInPage(userId, user);
                } else {
                    console.error('Error toggling user status');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }
    });

    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === editUserModal) {
            editUserModal.style.display = 'none';
        }
    });

    // Close modal when clicking cancel
    document.querySelector('.cancel').addEventListener('click', () => {
        editUserModal.style.display = 'none';
    });

    // Helper function to update user in page
    function updateUserInPage(userId, user) {
        const userCard = document.querySelector(`.user-card[data-id="${userId}"]`);
        if (userCard) {
            userCard.querySelector('h3').textContent = user.username;
            userCard.querySelector('p:nth-child(2)').textContent = `Email: ${user.email}`;
            userCard.querySelector('p:nth-child(4)').textContent = `Статус: ${user.is_active ? 'Активен' : 'Неактивен'}`;
            
            const toggleButton = userCard.querySelector('.toggle-status');
            toggleButton.textContent = user.is_active ? 'Деактивировать' : 'Активировать';
        }
    }
});