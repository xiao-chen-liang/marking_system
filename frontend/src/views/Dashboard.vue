<template>
  <div class="common-layout">
    <el-container>
      <el-header height="100px">
        <div class="header-content">
          <h1 class="headline">{{ headline }}</h1>
          <div class="user-info">
            <span class="username">{{ username }}</span>
            <el-button type="primary" @click="modifyPassword" class="modify-password-button">修改密码</el-button>
            <el-button type="primary" @click="logout" class="logout-button">退出登录</el-button>
          </div>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px" class="aside">
          <!-- Apply background color to el-menu -->
          <el-menu
            :default-active="activeIndex"
            class="el-menu-demo"
            mode="vertical"
            @select="handleSelect"
            style="background-color: #a0cfff;"
          >
            <!-- Apply custom styles to el-menu-item -->
            <el-menu-item
              index="1"
              style="font-size: 20px; display: flex; justify-content: center; align-items: center;"
            >
              成绩单
            </el-menu-item>
            <el-menu-item
              index="2"
              style="font-size: 20px; display: flex; justify-content: center; align-items: center;"
            >
              得分项
            </el-menu-item>
            <el-menu-item
              index="3"
              style="font-size: 20px; display: flex; justify-content: center; align-items: center;"
            >
              个人成绩
            </el-menu-item>
            <el-menu-item
              index="4"
              style="font-size: 20px; display: flex; justify-content: center; align-items: center;"
            >
              排名
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      msg: 'Welcome to Your Vue.js App',
      headline: '西南林业大学保研评分系统',
      activeIndex: '1',
      username: localStorage.getItem('username') || '' // Retrieve username from local storage
    }
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
      if (key === '1') {
        this.$router.push({name: 'report-card'})
      } else if (key === '2') {
        this.$router.push({name: 'score-item'})
      } else if (key === '3') {
        this.$router.push({name: 'score'})
      } else if (key === '4') {
        this.$router.push({name: 'ranking'})
      }
    },
    updateActiveIndex(route) {
      // Extract the index from the route's name or path
      switch (route.name) {
        case 'home':
          this.activeIndex = '1';
          break;
        case 'score-item':
          this.activeIndex = '2';
          break;
        case 'score':
          this.activeIndex = '3';
          break;
        default:
          this.activeIndex = '1'; // Default to the first item
      }
    },
    scrollToActiveItem() {
      // Scroll the menu to the active item if needed
      const el = document.querySelector(`.el-menu-item[index="${this.activeIndex}"]`);
      if (el) {
        el.scrollIntoView();
      }
    },
    logout() {
      // Handle the logout functionality
      localStorage.removeItem('username'); // Remove the username from localStorage
      localStorage.removeItem('userToken'); // Remove the token from localStorage
      this.$router.push('/login'); // Redirect to the login page
    },
    modifyPassword() {
      // Handle password modification functionality
      this.$router.push({ name: 'modify' }); // Redirect to the modify password page
    }
  },
  watch: {
    // Update activeIndex when the route changes
    $route(to, from) {
      this.updateActiveIndex(to);
    }
  },
  mounted() {
    // Ensure the menu is initially scrolled to the active item
    this.scrollToActiveItem();
  },
  updated() {
    // Ensure the menu is scrolled to the active item after navigation
    this.scrollToActiveItem();
  }
}
</script>

<style scoped>
.el-container {
  height: calc(100vh - 20px); /* Adjust for header height */
}

.el-header {
  background-color: #337ecc;
  display: flex;
  justify-content: center;
  align-items: center;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.headline {
  font-size: 48px;
}

.user-info {
  display: flex;
  align-items: center;
}

.username {
  font-size: 20px;
  margin-right: 20px;
}

.modify-password-button {
  margin-right: 20px;
}

.logout-button {
  margin-right: 20px;
}

.aside {
  background-color: #a0cfff; /* Background color for el-aside */
}

.el-main {
  background-color: #8bc4fe;
  height: 100%;
}
</style>
