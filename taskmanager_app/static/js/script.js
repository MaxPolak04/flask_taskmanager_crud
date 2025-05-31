const footerYear = document.querySelector('.current_year')
const nav = document.querySelector('.navbar-collapse')


document.addEventListener('DOMContentLoaded', function () {
    const createBtn = document.getElementById('create-task-button');
    if (createBtn) {
        createBtn.addEventListener('click', function () {
            const form = document.getElementById('createForm');
            if (form) {
                form.submit();
            }
        });
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.edit-task-button');
    editButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const taskId = btn.getAttribute('data-task-id');
            const form = document.getElementById(`editForm-${taskId}`);
            if (form) {
                form.submit();
            }
        });
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const createBtn = document.getElementById('create-user-button');
    if (createBtn) {
        createBtn.addEventListener('click', function () {
            const form = document.getElementById('createForm');
            if (form) {
                form.submit();
            }
        });
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.edit-user-button');
    editButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const userId = btn.getAttribute('data-user-id');
            const form = document.getElementById(`editForm-${userId}`);
            if (form) {
                form.submit();
            }
        });
    });
});


document.addEventListener('click', () => {
    if (nav.classList.contains('show')) {
        nav.classList.remove('show')
    }
})


const handleCurrentYear = () => {
    const year = new Date().getFullYear()
    footerYear.innerText = year
}

handleCurrentYear()