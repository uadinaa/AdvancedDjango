<template>
  <div class="container">
    <!-- Adding Item Section -->
    <div class="add-item">
      <h2>Adding Item</h2>
      <div class="input-container">
        <form @submit.prevent="addItem">
          <div class="input-wrapper">
            <input v-model="newItem.name" placeholder="Item Name" required />
          </div>
          <div class="input-wrapper">
            <input v-model="newItem.description" placeholder="Description" required />
          </div>
          <button type="submit">Add Item</button>
        </form>
      </div>
    </div>


    <div class="items-list">
      <h2>Items</h2>
      <ul>
        <li v-for="item in items" :key="item.id">
          <span class="item-name">{{ item.name }}</span>
          <span class="item-description">{{ item.description }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>

.container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background: #f4f1ff;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(128, 0, 128, 0.2);
  font-family: "Playfair Display", serif;
}


.add-item {
  background: linear-gradient(135deg, #8e44ad, #5e3370);
  padding: 20px;
  border-radius: 10px;
  color: white;
  text-align: center;
}

.add-item h2 {
  margin-bottom: 15px;
  font-size: 24px;
  font-weight: bold;
}


.input-container {
  background: rgba(255, 255, 255, 0.9);
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(255, 255, 255, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
}


.input-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}


.input-container input {
  width: 80%;
  padding: 12px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  text-align: center;
}


.add-item button {
  background: #e1bee7;
  color: #4a148c;
  border: none;
  padding: 12px 15px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 6px;
  width: 85%;
  margin-top: 10px;
}

.add-item button:hover {
  background: #ba68c8;
  color: white;
}


.items-list {
  margin-top: 20px;
  padding: 20px;
  background: white;
  border-radius: 10px;
}

.items-list h2 {
  color: #5e3370;
  font-size: 22px;
  margin-bottom: 10px;
  text-align: center;
}

.items-list ul {
  list-style: none;
  padding: 0;
}

.items-list li {
  display: flex;
  justify-content: space-between;
  padding: 12px;
  margin: 5px 0;
  background: #f8e6ff;
  border-radius: 8px;
  font-size: 18px;
}

.item-name {
  font-weight: bold;
  color: #4a148c;
}

.item-description {
  font-style: italic;
  color: #7b1fa2;
}
</style>




<script>
import { getItems, createItem } from '../api';

export default {
  data() {
    return {
      items: [],
      newItem: { name: '', description: '' },
    };
  },
  async created() {
    this.items = await getItems();
  },
  methods: {
    // async addItem() {
    //   const item = await createItem(this.newItem);
    //   this.items.push(item);
    //   this.newItem = { name: '', description: '' };
    // },
    async addItem() {
      const token = localStorage.getItem("authToken");

      const response = await fetch("http://127.0.0.1:8000/api/items/", {
        headers: { "Authorization": `Token ${token}` }
      });

      const data = await response.json();
      const item = await createItem(this.newItem);
      this.items.push(item);
      this.newItem = { name: '', description: '' };
      console.log(data);
    },

  },
};
</script>
