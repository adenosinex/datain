// Vue.js 应用主文件
const { createApp } = Vue;

createApp({
    delimiters: ['${', '}'],
    data() {
        return {
            currentTime: '',
            currentDate: '',
            loading: false,
            error: null,
            bookmarks: [],
            bookmarkCategories: [],
            newsData: [],
            techData: [],
            financeData: [],
            sportsData: [],
            entertainmentData: [],
            weatherData: {
                location: '',
                temperature: '',
                weather_desc: '',
                humidity: '',
                wind_speed: '',
                wind_direction: '',
                forecast: '',
                message: ''
            }
        }
    },
    computed: {
        allNewsData() {
            // 合并所有新闻数据
            const allData = [
                ...this.newsData,
                ...this.techData,
                ...this.financeData,
                ...this.sportsData,
                ...this.entertainmentData
            ];
            
            // 按时间排序（最新的在前）
            return allData.sort((a, b) => {
                const timeA = new Date(a.timestamp || 0);
                const timeB = new Date(b.timestamp || 0);
                return timeB - timeA;
            });
        }
    },
    methods: {
        updateTime() {
            const now = new Date();
            this.currentTime = now.toLocaleTimeString('zh-CN', {
                hour12: false,
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
            this.currentDate = now.toLocaleDateString('zh-CN', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                weekday: 'long'
            });
        },
        async loadData() {
            this.loading = true;
            this.error = null;
            
            try {
                // 并行加载所有新闻数据
                const [newsRes, techRes, financeRes] = await Promise.allSettled([
                    axios.get('/api/news'),
                    axios.get('/api/tech'),
                    axios.get('/api/finance')
                ]);
                
                // 处理新闻数据
                if (newsRes.status === 'fulfilled') {
                    this.newsData = newsRes.value.data.data || [];
                }
                
                if (techRes.status === 'fulfilled') {
                    this.techData = techRes.value.data.data || [];
                }
                
                if (financeRes.status === 'fulfilled') {
                    this.financeData = financeRes.value.data.data || [];
                }
                
                // 暂时使用模拟数据
                this.sportsData = [
                    { title: '体育新闻功能开发中...', link: '#', source: '系统', timestamp: new Date().toISOString() }
                ];
                
                this.entertainmentData = [
                    { title: '娱乐新闻功能开发中...', link: '#', source: '系统', timestamp: new Date().toISOString() }
                ];
                
            } catch (err) {
                this.error = '数据加载失败: ' + err.message;
                console.error('API Error:', err);
            } finally {
                this.loading = false;
            }
        },
        async loadBookmarks() {
            try {
                const response = await axios.get('/api/bookmarks');
                if (response.data.status === 'success') {
                    this.bookmarkCategories = response.data.data;
                    // 将所有书签扁平化到一个数组中
                    this.bookmarks = [];
                    this.bookmarkCategories.forEach(category => {
                        category.bookmarks.forEach(bookmark => {
                            this.bookmarks.push({
                                ...bookmark,
                                category: category.name,
                                categoryIcon: category.icon
                            });
                        });
                    });
                }
            } catch (err) {
                console.error('加载书签失败:', err);
            }
        },
        refreshData() {
            this.loadData();
        },
        async loadWeather() {
            try {
                const response = await axios.get('/api/weather');
                if (response.data.status === 'success') {
                    this.weatherData = response.data.data;
                }
            } catch (err) {
                console.error('Weather API Error:', err);
            }
        },
        formatTime(timestamp) {
            if (!timestamp) return '';
            const date = new Date(timestamp);
            return date.toLocaleString('zh-CN', {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
    },
                mounted() {
                // 更新时间
                this.updateTime();
                setInterval(this.updateTime, 1000);
                
                // 加载初始数据
                this.loadData();
                this.loadWeather();
                this.loadBookmarks();
                
                // 每5分钟自动刷新数据
                setInterval(this.loadData, 5 * 60 * 1000);
                
                // 每30分钟刷新天气数据
                setInterval(this.loadWeather, 30 * 60 * 1000);
            }
}).mount('#app');
