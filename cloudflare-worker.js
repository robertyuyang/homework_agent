// Cloudflare Worker - CORS 代理
// 部署到 Cloudflare Workers，免费且超级简单！

const COZE_API_URL = 'https://qz23wrnyv4.coze.site/stream_run';

export default {
  async fetch(request, env, ctx) {
    // 处理 CORS 预检请求
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
          'Access-Control-Max-Age': '86400',
        },
      });
    }

    // 只处理 POST 请求
    if (request.method !== 'POST') {
      return new Response(JSON.stringify({ error: 'Method not allowed' }), {
        status: 405,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    try {
      // 克隆请求以读取 body
      const requestBody = await request.json();
      
      // 获取 Authorization header
      const authHeader = request.headers.get('Authorization') || '';

      // 转发请求到 Coze API
      const cozeResponse = await fetch(COZE_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': authHeader,
        },
        body: JSON.stringify(requestBody),
      });

      // 获取响应
      const responseData = await cozeResponse.json();

      // 返回响应，添加 CORS 头
      return new Response(JSON.stringify(responseData), {
        status: cozeResponse.status,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
      });

    } catch (error) {
      console.error('Proxy error:', error);
      return new Response(JSON.stringify({
        error: 'Proxy error',
        message: error.message,
        content: `代理请求失败: ${error.message}`
      }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      });
    }
  },
};
