document.addEventListener('DOMContentLoaded', () => {
    const modalOverlay = document.querySelector('.modal-overlay');
    const closeModalButton = document.querySelector('.close-modal-button');
    const addHackathonModal = document.getElementById('addHackathonModal');
    const addHackathonForm = document.getElementById('addHackathonForm');
    const addButton = document.querySelector('.hackinfo-right-button');
    const userListButton = document.querySelector('.hackinfo-right-button-people');

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

    // Add Hackathon
    if (addButton) {
        addButton.addEventListener('click', (e) => {
            e.preventDefault();
            console.log('Add button clicked');
            if (addHackathonModal) {
                addHackathonModal.style.display = 'block';
                addHackathonModal.style.visibility = 'visible';
                console.log('Modal displayed');
            } else {
                console.error('Modal element not found');
            }
        });
    } else {
        console.error('Add button not found');
    }

    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === addHackathonModal) {
            addHackathonModal.style.display = 'none';
            addHackathonModal.style.visibility = 'hidden';
        }
    });

    // Close modal when clicking cancel
    document.querySelector('.cancel').addEventListener('click', () => {
        addHackathonModal.style.display = 'none';
        addHackathonModal.style.visibility = 'hidden';
    });

    // Handle form submission
    addHackathonForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(addHackathonForm);
        const csrftoken = getCookie('csrftoken');
        
        // Convert FormData to JSON object
        const data = {
            title: formData.get('title'),
            start_date: formData.get('start_date'),
            end_date: formData.get('end_date'),
            format: formData.get('format'),
            prize_fund: formData.get('prize_fund'),
            description: formData.get('description')
        };

        try {
            const response = await fetch('/api/hackathons/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const hackathon = await response.json();
                addHackathonToPage(hackathon);
                addHackathonModal.style.display = 'none';
                addHackathonModal.style.visibility = 'hidden';
                addHackathonForm.reset();
            } else {
                const error = await response.json();
                alert('Error adding hackathon: ' + error.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error adding hackathon. Please try again.');
        }
    });

    // Delete Hackathon
    document.addEventListener('click', async (e) => {
        if (e.target.classList.contains('delete-hack')) {
            e.preventDefault();
            if (confirm('Are you sure you want to delete this hackathon?')) {
                const hackathonBlock = e.target.closest('.activhack-block');
                const hackathonId = hackathonBlock.dataset.id;
                const csrftoken = getCookie('csrftoken');

                try {
                    const response = await fetch(`/api/hackathons/${hackathonId}/`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': csrftoken,
                        }
                    });

                    if (response.ok) {
                        hackathonBlock.remove();
                    } else {
                        console.error('Error deleting hackathon');
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            }
        }
    });

    // Edit Hackathon
    document.addEventListener('click', async (e) => {
        if (e.target.classList.contains('edit-hack')) {
            e.preventDefault();
            const hackathonBlock = e.target.closest('.activhack-block');
            const hackathonId = hackathonBlock.dataset.id;
            
            try {
                const response = await fetch(`/api/hackathons/${hackathonId}/`);
                const hackathon = await response.json();
                
                // Fill the form with hackathon data
                document.getElementById('title').value = hackathon.title;
                document.getElementById('start_date').value = hackathon.start_date;
                document.getElementById('end_date').value = hackathon.end_date;
                document.getElementById('format').value = hackathon.format;
                document.getElementById('prize_fund').value = hackathon.prize_fund;
                document.getElementById('description').value = hackathon.description;
                
                // Show the modal
                addHackathonModal.style.display = 'block';
                
                // Update form submission handler for editing
                const currentSubmitHandler = addHackathonForm.onsubmit;
                addHackathonForm.onsubmit = async (e) => {
                    e.preventDefault();
                    const formData = new FormData(addHackathonForm);
                    const csrftoken = getCookie('csrftoken');

                    const data = {
                        title: formData.get('title'),
                        start_date: formData.get('start_date'),
                        end_date: formData.get('end_date'),
                        format: formData.get('format'),
                        prize_fund: formData.get('prize_fund'),
                        description: formData.get('description')
                    };

                    try {
                        const response = await fetch(`/api/hackathons/${hackathonId}/`, {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrftoken,
                            },
                            body: JSON.stringify(data)
                        });

                        if (response.ok) {
                            const updatedHackathon = await response.json();
                            updateHackathonInPage(hackathonBlock, updatedHackathon);
                            addHackathonModal.style.display = 'none';
                            addHackathonForm.reset();
                            // Restore original submit handler
                            addHackathonForm.onsubmit = currentSubmitHandler;
                        } else {
                            const error = await response.json();
                            alert('Error updating hackathon: ' + error.error);
                        }
                    } catch (error) {
                        alert('Error updating hackathon. Please try again.');
                    }
                };
            } catch (error) {
                alert('Error loading hackathon data. Please try again.');
            }
        }
    });

    // Helper function to add new hackathon to page
    function addHackathonToPage(hackathon) {
        const template = `
            <div class="activhack-block" data-id="${hackathon.id}">
                <h3 class="activhack-text-up">${hackathon.title}</h3>
                <div class="activhack-info">
                    <div class="info-left">
                        <div class="left">
                            <p class="text">Date of the event: ${formatDate(hackathon.start_date)} - ${formatDate(hackathon.end_date)}</p>
                        </div>
                        <div class="left">
                            <p class="text">Event format: ${hackathon.format}</p>
                        </div>
                        <div class="left">
                            <p class="text">Prize pool: ${hackathon.prize_fund}</p>
                        </div>
                    </div>
                    <div class="info-right">
                        <p class="text">${hackathon.title}</p>
                        <p class="text">${hackathon.description.split('\n').join('<br>')}</p>
                        <p class="text">To do this, you need to assemble a team of up to four<br> people over the age of 18 and register it on the <br> website</p>
                        <div class="button">
                            <a href="#" class="link-hack edit-hack">Edit</a>
                            <a href="#" class="link-hack delete-hack">Delete</a>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.querySelector('.blocks').insertAdjacentHTML('beforeend', template);
    }

    // Helper function to update existing hackathon in page
    function updateHackathonInPage(hackathonBlock, hackathon) {
        hackathonBlock.querySelector('.activhack-text-up').textContent = hackathon.title;
        hackathonBlock.querySelector('.info-left .text:nth-child(1)').textContent = 
            `Date of the event: ${formatDate(hackathon.start_date)} - ${formatDate(hackathon.end_date)}`;
        hackathonBlock.querySelector('.info-left .text:nth-child(2)').textContent = 
            `Event format: ${hackathon.format}`;
        hackathonBlock.querySelector('.info-left .text:nth-child(3)').textContent = 
            `Prize pool: ${hackathon.prize_fund}`;
        hackathonBlock.querySelector('.info-right .text:nth-child(1)').textContent = 
            hackathon.title;
        hackathonBlock.querySelector('.info-right .text:nth-child(2)').innerHTML = 
            hackathon.description.split('\n').join('<br>');
        hackathonBlock.querySelector('.info-right .text:nth-child(3)').innerHTML = 
            'To do this, you need to assemble a team of up to four<br> people over the age of 18 and register it on the <br> website';
    }

    // Helper function to format date
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: '2-digit'
        });
    }

    // Original filter functionality
    function createDropdown(select) {
        const selected = select.querySelector('.select-selected');
        const items = select.querySelector('.select-items');

        selected.addEventListener('click', () => {
            items.style.display = items.style.display === 'block' ? 'none' : 'block';
        });

        items.addEventListener('click', (e) => {
            if (e.target.tagName === 'LI') {
                selected.textContent = e.target.textContent;
                items.style.display = 'none';
            }
        });
    }

    const openFilterButton = document.querySelector('.open-filter-button');
    openFilterButton.addEventListener('click', () => {
        modalOverlay.classList.add('active');
        modalOverlay.querySelector('.modal-content').classList.add('active');
        modalOverlay.querySelectorAll('.custom-select').forEach(createDropdown);
    });

    closeModalButton.addEventListener('click', () => {
        modalOverlay.classList.remove('active');
        modalOverlay.querySelector('.modal-content').classList.remove('active');
    });

    modalOverlay.addEventListener('click', (event) => {
        if (event.target === modalOverlay) {
            modalOverlay.classList.remove('active');
            modalOverlay.querySelector('.modal-content').classList.remove('active');
        }
    });

    document.querySelectorAll('.custom-select').forEach(createDropdown);

    document.querySelectorAll('.stek-item').forEach(item => {
        item.addEventListener('click', () => {
            item.classList.toggle('selected');
        });
    });

    // Handle user list button click
    userListButton.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = '/admin/users/';
    });
});















