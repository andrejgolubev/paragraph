import { loadSchedule } from "./loadSchedule.js";
import { setSelectedGroup } from "./datesDropdown.js";

let selectedGroupDataValue = null;

// ✅ ФУНКЦИЯ ДЛЯ ПОИСКА ГРУППЫ ПО НОМЕРУ
function findGroupByNumber(groupNumber) {
  return groups.find(group => 
    group.group_number.toLowerCase() === groupNumber.toLowerCase().trim()
  );
}

// ✅ ОБРАБОТЧИК НАЖАТИЯ ENTER
function handleEnterKey(event) {
  if (event.key === 'Enter') {
    event.preventDefault();
    
    const inputValue = searchInput.value.trim();
    if (!inputValue) return;
    
    // Ищем группу по введенному номеру
    const foundGroup = findGroupByNumber(inputValue);
    
    if (foundGroup) {
      // Если группа найдена - выбираем ее
      selectGroup(foundGroup.data_value, foundGroup.group_number);
    } else {
      // ✅ ЕСЛИ ГРУППА НЕ НАЙДЕНА - ПОКАЗЫВАЕМ СООБЩЕНИЕ
      showGroupNotFoundMessage(inputValue);
    }
    
    // Закрываем выпадающий список
    searchBody.classList.remove("active-search");
  }
}

// ✅ СООБЩЕНИЕ ЕСЛИ ГРУППА НЕ НАЙДЕНА
function showGroupNotFoundMessage(groupNumber) {
  const scheduleContainer = document.getElementById("schedule-container");
  const tipElem = document.querySelector(".tip"); 
  tipElem.classList.remove('tip-active')
  scheduleContainer.innerHTML = `
    <div class="error-message">
      <p>по запросу "<strong>${groupNumber}</strong>" информацией пока не располагаю :(</p>
      <p>убедитесь в правильности написания и повторите попытку</p>
    </div>
  `;
}

async function loadGroups() {
  try {
    const response = await fetch(
      "http://127.0.0.1:8000/schedule/get-all-groups"
    );
    return response.json();
  } catch (error) {
    console.error("Error loading groups:", error);
    return [];
  }
}

// Функция для выбора группы и сразу загрузки расписания
async function selectGroup(groupDataValue, groupNumber) {
  try {
    // Сохраняем группу на сервере
    const response = await fetch(
      "http://127.0.0.1:8000/schedule/select-group",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          group_data_value: groupDataValue,
        }),
      }
    );

    if (response.ok) {
      selectedGroupDataValue = groupDataValue;
      setSelectedGroup(groupDataValue); // cообщаем datesDropdown о выборе
      console.log("Group selected successfully");

      // СРАЗУ загружаем расписание для текущей даты
      await loadSchedule(groupDataValue);

      // Показываем блок выбора даты (опционально)
      document.getElementById("select-input").placeholder = "дата/неделя"; // спорно, нужна ли эта строка вообще
    }
  } catch (error) {
    console.error("Error selecting group:", error);
  }
}

const searchInput = document.getElementById("search-input");
const groupsList = document.getElementById("products");
const searchBody = document.querySelector(".search-block__body");

const groups = await loadGroups(); // 100: {group_number: '5876М', id: 101, data_value: '1401'}

//обработчик при клике по enter
searchInput.addEventListener("keydown", handleEnterKey);

searchInput.addEventListener("input", () => {
  const input = searchInput.value;
  groupsList.innerHTML = "";


  const filteredGroups = groups.filter((group) =>
    group.group_number.includes(input)
  );

  filteredGroups.forEach((group) => {
    const li = document.createElement("li");
    const link = document.createElement("a");

    link.textContent = group.group_number;
    link.href = `#`;

    // Обработчик выбора group
    li.addEventListener("click", async (event) => {
      event.preventDefault();

      //СРАЗУ выбираем группу и загружаем расписание
      await selectGroup(group.data_value, group.group_number);

      searchInput.value = group.group_number;

      searchBody.classList.remove("active-search");
    });

    li.appendChild(link);
    groupsList.appendChild(li);
  });

  if (input !== "" && filteredGroups.length > 0) {
    searchBody.classList.add("active-search");
  } else {
    searchBody.classList.remove("active-search");
  }
});

document.addEventListener("click", (event) => {
  if (
    !searchInput.contains(event.target) &&
    !groupsList.contains(event.target)
  ) {
    searchBody.classList.remove("active-search");
  }
});


