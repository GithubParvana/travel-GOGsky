// Home Ratings
let selectRatings = document.querySelector('#selectRatings')
let ratingsText = document.querySelector('#ratingsText')
let optionsRatings = document.querySelectorAll('.optionsRatings')
let listRatings = document.querySelector('#listRatings')

for(optionRating of optionsRatings){
    optionRating.onclick = function(){
        ratingsText.innerHTML = this.textContent
        listRatings.classList.toggle("show")
    }
}
selectRatings.onclick = function(){
    listRatings.classList.toggle("show")
}
// Home Ratings

// Home Nutrition
let selectNutrition = document.querySelector('#selectNutrition')
let nutritionText = document.querySelector('#nutritionText')
let optionsNutritions = document.querySelectorAll('.optionsNutritions')
let listNutritions = document.querySelector('#listNutritions')

for(optionNutrition of optionsNutritions){
    optionNutrition.onclick = function(){
        nutritionText.innerHTML = this.textContent
        listNutritions.classList.toggle("show")
    }
}
selectNutrition.onclick = function(){
    listNutritions.classList.toggle('show')
}
// Home Nutrition

// Home Nights
let selectNight = document.querySelector('#selectNight')
let nightText = document.querySelector('#nightText')
let listNight = document.querySelector('#listNight')
let optionsNights = document.querySelectorAll('.optionsNights')

for(optionNight of optionsNights){
    optionNight.onclick = function(){
        nightText.innerHTML = this.textContent
        listNight.classList.toggle('show')
    }
}
selectNight.onclick = function(){
    listNight.classList.toggle('show')
}
// Home Nights

// Home Guest
let selectGuest = document.querySelector('#selectGuest')
let guestText = document.querySelector('#guestText')
let listGuest = document.querySelector('#listGuest')
let adultCount = document.querySelector('#adultCount')
let adultIncrease = document.querySelector('#adultIncrease')
let adultDecrease = document.querySelector('#adultDecrease')
let childIncrease = document.querySelector('#childIncrease')
let childDecrease = document.querySelector('#childDecrease')
let childCount = document.querySelector('#childCount')



adultDecrease.onclick = function(){
    if(adultCount.innerHTML>0){
        adultCount.innerHTML = Number(adultCount.innerHTML)-1
    }
}
adultIncrease.onclick = function(){
    adultCount.innerHTML = Number(adultCount.innerHTML)+1
}

childDecrease.onclick = function(){
    if(childCount.innerHTML>0){
        childCount.innerHTML = Number(childCount.innerHTML)-1
    }
}
childIncrease.onclick = function(){
    childCount.innerHTML = Number(childCount.innerHTML)+1
}

selectGuest.onclick = function(){
    listGuest.classList.toggle("show")
    if(listGuest.classList.contains('show')){
        guestText.innerHTML = guestText.innerHTML
    }else if(adultCount.innerHTML>0 || childCount.innerHTML>0){
        guestText.innerHTML = `${adultCount.innerHTML} adult, ${childCount.innerHTML} child`
        
    }
}


// Home Guest

