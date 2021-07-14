document.addEventListener('DOMContentLoaded', function() {
    console.log('dom loaded');

    // Update trip to be available publicly or privately
    privacyBtn = document.querySelector('.privacy');
    if (privacyBtn) { // If button exists
        privacyBtn.onclick = () => { // this is either a 'Make it Public' or 'Keep it Private' button
            const tripID = parseInt(privacyBtn.dataset.tripid);
            const data = {
                purpose: 'privacy',
                tripID: tripID,
                // private = false if user hits 'Make it Public' button, and vice versa.
                private: (privacyBtn.innerHTML === 'Make it Public') ? false : true
            };

            fetch(`/trip/${tripID}/`, {
                method: "PUT",
                body: JSON.stringify(data)
            })
            .then(() => { // Reverse privacy button in front end
                privacyBtn.innerHTML = (privacyBtn.innerHTML === 'Make it Public') ? 'Keep it Private' : 'Make it Public';
            })
            .catch(error => {
                console.log("Error: ", error);
            });

        };
    }

    // Delete destination from specific trip on specific day
    document.querySelectorAll('.deleteDestinationBtn').forEach(button => {
        button.onclick = () => {
            console.log('Delete destination btn clicked');
            const tripID = parseInt(button.dataset.tripid);
            const tripDetailID = parseInt(button.dataset.tripdetailid);
            const destinationID = parseInt(button.dataset.destinationid);
            const data = {
                purpose: 'deleteActivity',
                tripDetailID: tripDetailID,
                destinationID: destinationID
            };

            fetch(`/trip/${tripID}/`, {
                method: "PUT",
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => { // Remove activity in front end
                
                if (result.error !== undefined) {
                    alert(`${result.error}`);
                } else {
                    const placeWrapper = button.closest('.place');
                    placeWrapper.style.animationPlayState = 'running';
                    placeWrapper.addEventListener('animationend', () => {
                        placeWrapper.remove();
                    });
                }
            })
            .catch(error => {
                console.log("Error: ", error);
            });

        };
    });

    // Add destination to specific trip on specific day
    // Customize modals based on destination name
    document.querySelectorAll('.add-destinationBtn').forEach(button => {
        button.onclick = () => {
            const name = button.dataset.name;
            const city = button.dataset.city;
            const region = button.dataset.region;
            const modal = document.querySelector('#destinationModal');
            modal.querySelector('#modalTitle').innerHTML = name; // Populate modal header

            // Populate values for hidden inputs (to extract data in back end later on)
            modal.querySelector('#input-hidden-name').setAttribute("value", name);
            modal.querySelector('#input-hidden-city').setAttribute("value", city);
            modal.querySelector('#input-hidden-region').setAttribute("value", region);
        };
    });

});


// Turns out this is not needed as API is contacted from backend instead
// document.querySelector('#test-api').onclick = () => {
//     fetch('https://api.windy.com/api/webcams/v2/list/country=IT?show=', {
//         method: "GET",
//         headers: {
//             "x-windy-key": 'your API key
//         }
//     })
//     .then(response => response.json())
//     .then(result => {
//         console.log(result);
//     })
//     .catch(error => {
//         console.log('error', error);
//     });
// };
