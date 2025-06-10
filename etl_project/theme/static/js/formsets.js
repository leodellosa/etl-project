document.addEventListener('DOMContentLoaded', function () {
  const addLevelBtn = document.getElementById('add-level');
  const levelsContainer = document.getElementById('levels-formset');
  let levelFormIndex = document.querySelectorAll('[data-level-index]').length;

  // Add Level
  addLevelBtn.addEventListener('click', function () {
    const newForm = levelsContainer.querySelector('[data-level-index="0"]').cloneNode(true);
    newForm.dataset.levelIndex = levelFormIndex;

    // Clear inputs and update names/ids
    newForm.querySelectorAll('input, select, textarea').forEach(input => {
      if (input.type !== 'hidden') input.value = '';
      if (input.name) input.name = input.name.replace(/-\d+-/, `-${levelFormIndex}-`);
      if (input.id) input.id = input.id.replace(/-\d+-/, `-${levelFormIndex}-`);
    });

    // Update management form TOTAL_FORMS
    const totalForms = document.querySelector('#id_levels-TOTAL_FORMS');
    totalForms.value = parseInt(totalForms.value) + 1;

    // Update category container ID if present
    const catContainer = newForm.querySelector('.categories-container');
    if (catContainer) catContainer.id = `categories-${levelFormIndex}`;

    // Remove any nested forms (categories/items) except the first, and clear their values
    newForm.querySelectorAll('.category-form:not(:first-child)').forEach(cat => cat.remove());
    newForm.querySelectorAll('.category-form input, .category-form select, .category-form textarea').forEach(input => {
      if (input.type !== 'hidden') input.value = '';
    });

    // Add remove button if not present
    if (!newForm.querySelector('.remove-level')) {
      const removeBtn = document.createElement('button');
      removeBtn.type = 'button';
      removeBtn.className = 'remove-level btn btn-danger ml-2';
      removeBtn.textContent = 'Remove';
      removeBtn.addEventListener('click', function () {
        newForm.remove();
        totalForms.value = parseInt(totalForms.value) - 1;
      });
      newForm.appendChild(removeBtn);
    }

    levelsContainer.appendChild(newForm);
    levelFormIndex++;

    const allLevelHeadings = levelsContainer.querySelectorAll('.level-heading');
    allLevelHeadings.forEach((heading, idx) => {
        heading.textContent = `Level ${idx + 1}`;
    });

    // Attach add-category event to the new level's button
    const addCatBtn = newForm.querySelector('.add-category-btn');
    if (addCatBtn) {
      addCatBtn.addEventListener('click', handleAddCategory);
    }
  });

  // Attach to existing add-category buttons
  document.querySelectorAll('.add-category-btn').forEach(btn => {
    btn.addEventListener('click', handleAddCategory);
  });

  // Add Category Handler
  function handleAddCategory(e) {
    e.preventDefault();
    const btn = e.currentTarget || e.target;
    const levelDiv = btn.closest('[data-level-index]');
    const categoriesContainer = levelDiv.querySelector('.categories-container');
    const template = document.getElementById('category-template');
    const newCategory = template.cloneNode(true);
    newCategory.classList.remove('hidden');
    newCategory.removeAttribute('id');

    // Update input names/ids for Django formset compatibility
    const levelIndex = levelDiv.dataset.levelIndex;
    const categoryCount = categoriesContainer.querySelectorAll('.category-form').length;

    newCategory.querySelectorAll('select, input, textarea').forEach(input => {
    // For the category select
    if (input.matches('select')) {
        input.name = `categories-${levelIndex}-${categoryCount}-name`;
        input.id = `id_categories-${levelIndex}-${categoryCount}-name`;
    }
    // For item management forms and containers:
    if (input.name && input.name.includes('items-__level__-__cat__')) {
        input.name = input.name.replace('__level__', levelIndex).replace('__cat__', categoryCount);
        input.id = input.id.replace('__level__', levelIndex).replace('__cat__', categoryCount);
    }
    });

    // Update items container ID
    const itemsContainer = newCategory.querySelector('.items-container');
    if (itemsContainer) {
      itemsContainer.id = `items-${levelIndex}-${categoryCount}`;
    }

    // Update Add Item button data attributes
    const addItemBtn = newCategory.querySelector('.add-item-btn');
    if (addItemBtn) {
      addItemBtn.dataset.level = levelIndex;
      addItemBtn.dataset.cat = categoryCount;
    }

    // Add remove logic for this category
    const removeBtn = newCategory.querySelector('.remove-category-btn');
    if (removeBtn) {
      removeBtn.addEventListener('click', function () {
        newCategory.remove();
        // Update TOTAL_FORMS after removal
        const totalFormsInput = levelDiv.querySelector(`input[name="categories-${levelIndex}-TOTAL_FORMS"]`);
        if (totalFormsInput) {
          totalFormsInput.value = categoriesContainer.querySelectorAll('.category-form').length;
        }
      });
    }

    // Append to the container
    categoriesContainer.appendChild(newCategory);

    // Update management form
    const totalFormsInput = levelDiv.querySelector(`input[name="categories-${levelIndex}-TOTAL_FORMS"]`);
    if (totalFormsInput) {
      totalFormsInput.value = categoriesContainer.querySelectorAll('.category-form').length;
    }
  }

  // Attach remove event to existing remove-level buttons (if any)
  document.querySelectorAll('.remove-level').forEach(btn => {
    btn.addEventListener('click', function () {
      btn.closest('[data-level-index]').remove();
      const totalForms = document.querySelector('#id_levels-TOTAL_FORMS');
      totalForms.value = parseInt(totalForms.value) - 1;
    });
  });

  // Add Item Handler
  function handleAddItem(e) {
    e.preventDefault();
    const btn = e.target;
    const levelIndex = btn.dataset.level;
    const catIndex = btn.dataset.cat;
    const categoryDiv = btn.closest('.category-form');
    const itemsContainer = categoryDiv.querySelector('.items-container');
    const template = document.getElementById('item-template');
    const newItem = template.cloneNode(true);
    newItem.classList.remove('hidden');
    newItem.removeAttribute('id');

    // Update input names/ids
    const itemCount = itemsContainer.querySelectorAll('.item-form').length;
    newItem.querySelectorAll('input, select, textarea').forEach(input => {
      if (input.name) input.name = `items-${levelIndex}-${catIndex}-${itemCount}-name`;
      if (input.id) input.id = `id_items-${levelIndex}-${catIndex}-${itemCount}-name`;
      input.value = '';
    });

    // Remove logic
    const removeBtn = newItem.querySelector('.remove-item-btn');
    if (removeBtn) {
      removeBtn.addEventListener('click', function () {
        newItem.remove();
        // Update management form after removal
        const totalFormsInput = categoryDiv.querySelector(`input[name="items-${levelIndex}-${catIndex}-TOTAL_FORMS"]`);
        if (totalFormsInput) {
          totalFormsInput.value = itemsContainer.querySelectorAll('.item-form').length;
        }
      });
    }

    itemsContainer.appendChild(newItem);

    // Update management form
    const totalFormsInput = categoryDiv.querySelector(`input[name="items-${levelIndex}-${catIndex}-TOTAL_FORMS"]`);
    if (totalFormsInput) {
      totalFormsInput.value = itemsContainer.querySelectorAll('.item-form').length;
    }
  }

  // Attach to all add-item-btns (event delegation)
  document.addEventListener('click', function(e) {
    if (e.target && e.target.classList.contains('add-item-btn')) {
      handleAddItem(e);
    }
  });
});