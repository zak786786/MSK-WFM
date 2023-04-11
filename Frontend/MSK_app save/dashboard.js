// could use toastify to notice updates?



// running the dashboard commands, might need preload func

const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const btnPopupclose = document.querySelector('.icon-close');
const second_page = document.querySelector('.second_page');
const button_1 = document.querySelector('.button_1');

    // for login + X
    btnPopup.addEventListener('click', ()=> {
        wrapper.classList.remove('active-closepopup');
        wrapper.classList.add('active-popup');
    });
    btnPopupclose.addEventListener('click', ()=> {
        wrapper.classList.remove('active-popup');
        wrapper.classList.add('active-closepopup');
    });

    //for second page
    button_1.addEventListener('click', ()=> {
       if (second_page.classList.contains('active')){
        second_page.classList.remove('active');
        second_page.classList.add('hidden');
       } else {
        second_page.classList.remove('hidden');
        second_page.classList.add('active');
       }
    });
    