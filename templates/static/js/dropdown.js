async function loadGroups() {
  try {
    const response = await fetch(
      "http://127.0.0.1:8000/schedule/get-all-groups"
    );
    const groups = await response.json();
    return groups;
  } catch (error) {
    console.error("Error loading groups:", error);
    return [];
  }
}

const searchInput = document.getElementById("search-input");
const groupsList = document.getElementById("products");
const searchBody = document.querySelector(".search-block__body");

const groups = await loadGroups(); // 100: {group_number: '5876М', id: 101, data_value: '1401'}

groups.forEach((element) => {
  console.log(element); // выводит все номера групп
});

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
    link.href = `https://rasp.rsreu.ru/schedule-frame/group?faculty=0&group=${group.data_value}`; // ЭТО РОФЛС))0)

    link.target = "_blank"; // убрать когда уберешь рофлс сверху

    li.appendChild(link);
    groupsList.appendChild(li);
  });

  if (input !== "" && filteredGroups.length > 0){
    searchBody.classList.add('active-search') 
  }else{
    searchBody.classList.remove('active-search')
  }
});
