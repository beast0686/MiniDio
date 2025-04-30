document.addEventListener('DOMContentLoaded', function() {
    const inputField = document.querySelector('.input-field');
    const meetingItems = document.querySelectorAll('.meeting-item');
    const meetingDeleteBtns = document.querySelectorAll('.meeting-delete-btn');
    const clearSectionBtns = document.querySelectorAll('.clear-section');
    const toggleSearchBtn = document.getElementById('toggle-search-btn');
    const searchContainer = document.getElementById('search-container');
    const searchResults = document.getElementById('search-results');
    const searchButton = document.getElementById('search-button');
    const searchInput = document.querySelector('.search-input');
    const welcomeContainer = document.getElementById('welcome-container');
    const clearSearchHistory = document.getElementById('clear-search-history');

    // Auto-resize textarea
    inputField.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Send message on Enter (without Shift)
    inputField.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Meeting items click handler
    meetingItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // Don't select if clicking the delete button
            if (e.target.closest('.meeting-delete-btn')) {
                return;
            }

            // Highlight selected item
            meetingItems.forEach(mi => mi.classList.remove('selected'));
            this.classList.add('selected');

            // In a real app, load the meeting notes here
            console.log("Selected meeting:", this.textContent.trim());
        });
    });

    // Delete meeting item handler
    meetingDeleteBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const meetingItem = this.closest('.meeting-item');
            const meetingId = this.getAttribute('data-id');

            // Animation for deletion
            meetingItem.style.opacity = '0.5';
            setTimeout(() => {
                meetingItem.remove();
            }, 300);

            console.log("Deleted meeting:", meetingId);
        });
    });

    // Clear section handler
    clearSectionBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const section = this.getAttribute('data-section');
            const dateSection = this.closest('.date-section');
            const items = dateSection.querySelectorAll('.meeting-item');

            items.forEach(item => {
                item.style.opacity = '0.5';
            });

            setTimeout(() => {
                items.forEach(item => {
                    item.remove();
                });
            }, 300);

            console.log("Cleared section:", section);
        });
    });

    // Toggle search container
    toggleSearchBtn.addEventListener('click', function() {
        if (searchContainer.style.display === 'none') {
            searchContainer.style.display = 'flex';
            welcomeContainer.style.display = 'none';
            searchInput.focus();
        } else {
            searchContainer.style.display = 'none';
            searchResults.style.display = 'none';
            welcomeContainer.style.display = 'flex';
        }
    });

    // Search button handler
    searchButton.addEventListener('click', function() {
        toggleSearchBtn.click();
    });

    // Search input handler
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        if (query) {
            searchResults.style.display = 'block';
            // In a real app, perform actual search here
        } else {
            searchResults.style.display = 'none';
        }
    });

    // Clear search history
    clearSearchHistory.addEventListener('click', function() {
        const searchResultItems = document.querySelectorAll('.search-result-item');
        searchResultItems.forEach(item => {
            item.style.opacity = '0.5';
        });

        setTimeout(() => {
            searchResultItems.forEach(item => {
                item.remove();
            });
            searchResults.style.display = 'none';
        }, 300);

        console.log("Cleared search history");
    });

    // Search result item delete buttons
    document.querySelectorAll('.search-result-item .meeting-delete-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const resultItem = this.closest('.search-result-item');

            resultItem.style.opacity = '0.5';
            setTimeout(() => {
                resultItem.remove();
                if (document.querySelectorAll('.search-result-item').length === 0) {
                    searchResults.style.display = 'none';
                }
            }, 300);
        });
    });

    // Click on search result item
    document.querySelectorAll('.search-result-item').forEach(item => {
        item.addEventListener('click', function(e) {
            if (e.target.closest('.meeting-delete-btn')) {
                return;
            }

            // In a real app, load this search result
            console.log("Selected search result:", this.textContent.trim());

            // Close search and show the selected result
            searchContainer.style.display = 'none';
            searchResults.style.display = 'none';
            welcomeContainer.style.display = 'none';

            // Here you would display the actual content
        });
    });

    function sendMessage() {
        const message = inputField.value.trim();
        if (message === '') return;

        // Add to search history
        const searchTerm = message;
        const now = new Date();

        // In a real app, you would process the message and store it
        console.log("Recording meeting notes:", message);

        // Clear input
        inputField.value = '';
        inputField.style.height = 'auto';

        // Create a new meeting item and add it to Today section
        const newMeetingItem = document.createElement('div');
        newMeetingItem.className = 'meeting-item';
        newMeetingItem.innerHTML = `
                    ${searchTerm.substring(0, 30)}${searchTerm.length > 30 ? '...' : ''}
                    <div class="meeting-actions">
                        <button class="meeting-delete-btn" data-id="new-meeting-${Date.now()}">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                    </div>
                `;

        // Add to today section
        const todaySection = document.querySelector('.date-section:first-of-type');
        const items = todaySection.querySelectorAll('.meeting-item');
        if (items.length > 0) {
            todaySection.insertBefore(newMeetingItem, items[0]);
        } else {
            todaySection.appendChild(newMeetingItem);
        }

        // Add event listeners to the new item
        newMeetingItem.addEventListener('click', function(e) {
            if (e.target.closest('.meeting-delete-btn')) {
                return;
            }
            meetingItems.forEach(mi => mi.classList.remove('selected'));
            this.classList.add('selected');
        });

        newMeetingItem.querySelector('.meeting-delete-btn').addEventListener('click', function(e) {
            e.stopPropagation();
            const meetingItem = this.closest('.meeting-item');
            meetingItem.style.opacity = '0.5';
            setTimeout(() => {
                meetingItem.remove();
            }, 300);
        });
    }

    // Focus the input field on page load
    inputField.focus();
});