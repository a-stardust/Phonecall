
    document.addEventListener('DOMContentLoaded', function () {
        const checkboxes = document.querySelectorAll('.call-checkbox');
        const schoolList = document.querySelector('.school-list');
        const schoolItems = Array.from(document.querySelectorAll('.school-item'));

        // Load saved checkbox states from localStorage and mark completed items
        checkboxes.forEach(checkbox => {
            const index = checkbox.dataset.index;
            const savedState = localStorage.getItem(`checkbox-${index}`);
            const schoolItem = document.getElementById('school-' + index);

            if (savedState === 'checked') {
                checkbox.checked = true;
                schoolItem.classList.add('completed');
            }
        });

        // Separate items into checked and unchecked groups
        const uncheckedItems = schoolItems.filter(item => !item.querySelector('.call-checkbox').checked);
        const checkedItems = schoolItems.filter(item => item.querySelector('.call-checkbox').checked);

        // Sort unchecked items by their original IDs
        uncheckedItems.sort((a, b) => {
            return parseInt(a.id.split('-')[1]) - parseInt(b.id.split('-')[1]);
        });

        // Append unchecked items first, followed by checked items in their current order
        uncheckedItems.forEach(item => {
            schoolList.appendChild(item);
        });
        checkedItems.forEach(item => {
            schoolList.appendChild(item);
        });

        // Add event listener for checkbox changes
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function () {
                const schoolItem = document.getElementById('school-' + this.dataset.index);

                if (this.checked) {
                    // Move checked item to the end and save the state
                    schoolItem.classList.add('completed');
                    schoolList.appendChild(schoolItem);
                    localStorage.setItem(`checkbox-${this.dataset.index}`, 'checked');
                } else {
                    // Remove completed class and save the state
                    schoolItem.classList.remove('completed');
                    localStorage.setItem(`checkbox-${this.dataset.index}`, 'unchecked');

                    // Re-sort and re-append unchecked items while maintaining order of checked items
                    const updatedUncheckedItems = Array.from(document.querySelectorAll('.school-item'))
                        .filter(item => !item.querySelector('.call-checkbox').checked);
                    const updatedCheckedItems = Array.from(document.querySelectorAll('.school-item'))
                        .filter(item => item.querySelector('.call-checkbox').checked);

                    updatedUncheckedItems.sort((a, b) => {
                        return parseInt(a.id.split('-')[1]) - parseInt(b.id.split('-')[1]);
                    });

                    updatedUncheckedItems.forEach(item => {
                        schoolList.appendChild(item);
                    });
                    updatedCheckedItems.forEach(item => {
                        schoolList.appendChild(item);
                    });
                }
            });
        });
    });
    