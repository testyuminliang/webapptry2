// 当整个HTML文档加载完成后，再执行我们的代码
document.addEventListener('DOMContentLoaded', () => {

    // 通过ID找到HTML里的按钮和数据显示容器
    const fetchButton = document.getElementById('fetch-user-btn');
    const userContainer = document.getElementById('user-container');

    // 给按钮添加一个“点击”事件的监听器
    fetchButton.addEventListener('click', () => {
        
        userContainer.textContent = '正在从API加载数据...';

        // 使用 fetch API 向我们的Flask后端发送请求
        // 这就是前端JS在调用后端API！
        fetch('/api/user')
            .then(response => {
                // 检查请求是否成功
                if (!response.ok) {
                    throw new Error('网络响应错误');
                }
                // 将响应体解析为JSON
                return response.json();
            })
            .then(data => {
                // 成功获取并解析数据后，将数据显示在页面上
                // JSON.stringify(data, null, 2) 是为了让JSON格式化后更好看
                userContainer.textContent = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                // 如果过程中出现任何错误，在这里捕获并显示
                console.error('获取数据失败:', error);
                userContainer.textContent = '获取数据失败，请查看控制台获取更多信息。';
            });
    });
});