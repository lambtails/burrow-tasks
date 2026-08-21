/**
 * Task handling code
 * Sends updates to the server to tell it a task is done
 */
const updateTask = (id, done = false) => {
    const url = "/update";
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            row_id: id,
            done: done,
        }),
    };
    fetch(url, options)
        .then((response) => response.text())
        .catch((error) => console.error("Error:", error));
};

document.querySelectorAll("input[type=checkbox]").forEach((checkbox) => {
    checkbox.addEventListener("input", (e) => {
        const elem = e.target;
        const rowid = parseInt(elem.id.split("-")[1]);
        updateTask(rowid, (done = elem.checked));
    });
});

/**
 * Dragging items around logic
 * Based on some code I found online
 * Might not end up using this but it's still helpful to have!
 */
const sortable_list = document.querySelector(".sortable-list");
let drag_elem = null;

sortable_list.addEventListener("dragstart", (e) => {
    // Begin dragging item
    drag_elem = e.target;
    e.target.classList.add("dragging");
});

sortable_list.addEventListener("dragend", (e) => {
    // Drop item to cancel dragging
    // If the list has been re-ordered due to dragging, this will keep it in the new spot!
    e.target.classList.remove("dragging");
    document
        .querySelectorAll(".sortable-item")
        .forEach((item) => item.classList.remove("over"));
    drag_elem = null;
});

sortable_list.addEventListener("dragover", (e) => {
    // Dragging the item over the list will rearrange it dynamically
    e.preventDefault();

    // Clear drag over state from all elements
    document
        .querySelectorAll(".sortable-item")
        .forEach((item) => item.classList.remove("over"));

    // Identify which element is being dragged over
    const drag_over_elem = getDragAfterElement(sortable_list, e.clientY);

    // Check if item is being dragged over another element
    if (drag_over_elem) {
        drag_over_elem.classList.add("over");
        sortable_list.insertBefore(drag_elem, drag_over_elem);
    } else {
        sortable_list.appendChild(drag_elem);
    }
});

function getDragAfterElement(container, y) {
    // Function to identify which elements are underneath the drag item
    const draggable_elems = [
        ...container.querySelectorAll(".sortable-item:not(.dragging)"),
    ];
    return draggable_elems.reduce(
        (closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else {
                return closest;
            }
        },
        { offset: Number.NEGATIVE_INFINITY },
    ).element;
}

/**
 * Other miscellaneous code
 */
// This prevents the browser from asking to resend form data
// It's a bit hacky but works perfectly fine for this project :)
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
