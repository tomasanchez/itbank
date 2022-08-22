const categories = document.querySelectorAll('#categories .category');
const containerQuestions = document.querySelectorAll('.container-questions');
let categorieActive = null;

categories.forEach((category) => {
    category.addEventListener('click', (e) => {
        categories.forEach((element => {
            element.classList.remove('active');
        }))

        e.currentTarget.classList.toggle('active');
        categorieActive = category.dataset.category;


        //active the question container. 
        containerQuestions.forEach((container) => {
            if (container.dataset.category === categorieActive) {
                container.classList.add('active');
            } else {
                container.classList.remove('active');
            }
        })
    })
}) 

//Now questions
const questions = document.querySelectorAll('.questions .container-question');
questions.forEach((question) => {
    question.addEventListener('click', (z) => {
        z.currentTarget.classList.toggle('active');


        const answer = question.querySelector('.answer');
        const heightAnswer = answer.scrollHeight;
        
        if (!answer.style.maxHeight) {
            answer.style.maxHeight = heightAnswer + 'px';
            
        } else {
            answer.style.maxHeight = null;
        }
        
        questions.forEach((element) => {
            if (question !== element) {
             element.classList.remove('active');
             element.querySelector('.answer').style.maxHeight = null;   
            }
        })


    })
})
