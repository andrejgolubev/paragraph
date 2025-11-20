import { loadSchedule } from "./loadSchedule.js";
import { setSelectedGroup } from "./datesDropdown.js";

let selectedGroupDataValue = null;

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
