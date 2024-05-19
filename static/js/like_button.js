async function addToCollection(problem_id) {
    try {
        const response = await fetch('/add_to_collection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ problem_id: problem_id })
        });
        const result = await response.json();
        console.log(result.message);
    } catch (error) {
        console.error('Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const likeButton = document.querySelector('.Btn');
    likeButton.addEventListener('click', function() {
        const problem_id = new URL(location.href).searchParams.get('problem_id');  // 取得problem_id
        addToCollection(problem_id);
    });
});
