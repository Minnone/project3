document.addEventListener('DOMContentLoaded', () => {
    const modalOverlay = document.querySelector('.modal-overlay');
    const closeModalButton = document.querySelector('.close-modal-button');
  
    // Функция для создания выпадающего списка
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
  
    // Обработчик открытия модального окна
    const openFilterButton = document.querySelector('.open-filter-button');
    openFilterButton.addEventListener('click', () => {
        modalOverlay.classList.add('active');
        modalOverlay.querySelector('.modal-content').classList.add('active');
        modalOverlay.querySelectorAll('.custom-select').forEach(createDropdown);
    });
  
    // Обработчик закрытия модального окна
    closeModalButton.addEventListener('click', () => {
        modalOverlay.classList.remove('active');
        modalOverlay.querySelector('.modal-content').classList.remove('active');
    });

    // Обработчик клика вне модального окна
    modalOverlay.addEventListener('click', (event) => {
        if (event.target === modalOverlay) {
            modalOverlay.classList.remove('active');
            modalOverlay.querySelector('.modal-content').classList.remove('active');
        }
    });

    // Инициализация выпадающих списков на странице
    document.querySelectorAll('.custom-select').forEach(createDropdown);

    // Добавленные части кода

    // Обработка кликов на элементах стека
    document.querySelectorAll('.stek-item').forEach(item => {
        item.addEventListener('click', () => {
            // Переключаем класс 'selected' на нажатом элементе
            item.classList.toggle('selected');
        });
    });

    // Переключение навигационного меню
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.desktop-nav');

    if (menuToggle && nav) {
        menuToggle.addEventListener('click', () => {
            nav.classList.toggle('active');
        });
    }
});
