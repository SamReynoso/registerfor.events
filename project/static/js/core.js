
function openAppDropdown(event) {
    event.preventDefault();
    const dropdown = document.getElementById(event.target.dataset.toggle);
    if (dropdown) {
        const openDropdown = document.querySelector('.collapse-navigation-list.open');
        if (openDropdown && openDropdown !== dropdown) {
            openDropdown.classList.remove('open');
        }
        dropdown.classList.toggle('open');
    } else {
        console.error("Dropdown with ID " + event.target.dataset.toggle + " not found.");
    }
}

/* close open dropdowns whenever there is a click */
window.addEventListener('click', function(event) {
    if (event.target.dataset.toggle) {
        return;
    }
    const openDropdown = document.querySelector('.collapse-navigation-list.open');
    if (openDropdown) {
        openDropdown.classList.remove('open');
    }
});

/* scroll down to the summary when details are toggled */
window.addEventListener('toggle', function(event) {
    const details = event.target;

    if (details.tagName === 'DETAILS' && details.open) {
        const summary = details.querySelector('summary');
        if (summary) {
            summary.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});

function handleClose() {
    const openDropdown = document.querySelector('.collapse-navigation-list.open');
    if (openDropdown) {
        openDropdown.classList.remove('open');
    }
    const sidebar = document.getElementById('sidebar');
    if (sidebar && sidebar.classList.contains('slide-in')) {
        sidebar.classList.remove('slide-in');
    }
    const mutedOverlay = document.getElementById('mutedOverlay');
    if (mutedOverlay) {
        mutedOverlay.classList.remove('active');
    }
    const navbarDropdown = document.getElementById('navbarDropdown');
    if (navbarDropdown && navbarDropdown.classList.contains('show')) {
        navbarDropdown.classList.remove('show');
    }
    const navbarDropdownArrow = document.getElementById('navbarDropdowArrow');
    if (navbarDropdownArrow && navbarDropdownArrow.classList.contains('rotate')) {
        navbarDropdownArrow.classList.remove('rotate');
    }
}


document.addEventListener("blur", function(event) {
    handleClose();
});

document.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        handleClose();
        return;
    }

    const focused = document.activeElement;
});

function toggleOrRemoveClass(element, toggleElement, className, event, overlay=null) {
    if (toggleElement.contains(event.target)) {
        element.classList.toggle(className);
        if (overlay) {
            overlay.classList.toggle('active');
        }
    } else if (!element.contains(event.target)) {
        element.classList.remove(className);
        if (overlay) {
            overlay.classList.remove('active');
        }
    } else {
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const navbarDropdownToggle = document.getElementById('navbarDropdowToggle');
    const navbarDropdown = document.getElementById('navbarDropdown');
    const mutedOverlay = document.getElementById('mutedOverlay');
    const navbarDropdownArrow = document.getElementById('navbarDropdowArrow');

    document.addEventListener('click', (event) => {
        toggleOrRemoveClass(sidebar, sidebarToggle, 'slide-in', event, mutedOverlay);
        toggleOrRemoveClass(navbarDropdown, navbarDropdownToggle, 'show', event);
        toggleOrRemoveClass(navbarDropdownArrow, navbarDropdownToggle, 'rotate', event);
    });

});

