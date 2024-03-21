const table = document.getElementById('problem_list');
const rowsPerPage = 5; // 每頁顯示的行數
const totalRows = table.rows.length - 1; // 減去表頭行
const pagination = document.getElementById('pagination');
const previousPage = document.getElementById('previousPage');
const nextPage = document.getElementById('nextPage');
let currentPage = 1;

function displayRows(page) {
    const startIndex = (page - 1) * rowsPerPage + 1;
    const endIndex = Math.min(startIndex + rowsPerPage - 1, totalRows);

    for (let i = 1; i <= totalRows; i++) {
        const row = table.rows[i];
        if (i >= startIndex && i <= endIndex) {
            row.classList.remove('d-none');
        } else {
            row.classList.add('d-none');
        }
    }
}

function createPagination() {
    const numPages = Math.ceil(totalRows / rowsPerPage);
    let paginationHTML = '';

    paginationHTML += `<li class="page-item" id="previousPage">
      <a class="page-link" href="#" aria-label="Previous">
        <span aria-hidden="true">&laquo;</span>
      </a>
    </li>`;

    // 僅顯示第1、2、3頁以及最後一頁的分頁按鈕
    for (let i = 1; i <= Math.min(numPages, 3); i++) {
        paginationHTML += `<li class="page-item"><a class="page-link" href="#" onclick="displayRows(${i})">${i}</a></li>`;
    }

    // 添加省略符號
    if (numPages > 3) {
        paginationHTML += `<li class="page-item disabled"><a class="page-link" href="#">...</a></li>`;
    }

    paginationHTML += `<li class="page-item"><a class="page-link" href="#" onclick="displayRows(${numPages})">${numPages}</a></li>`;

    paginationHTML += `<li class="page-item" id="nextPage">
      <a class="page-link" href="#" aria-label="Next">
        <span aria-hidden="true">&raquo;</span>
      </a>
    </li>`;

    pagination.innerHTML = paginationHTML;
}

// 初始顯示第1頁
displayRows(1);
// 創建分頁按鈕
createPagination();

previousPage.addEventListener('click', function () {
    if (currentPage > 1) {
        currentPage--;
        displayRows(currentPage);
    }
});

nextPage.addEventListener('click', function () {
    if (currentPage < Math.ceil(totalRows / rowsPerPage)) {
        currentPage++;
        displayRows(currentPage);
    }
});