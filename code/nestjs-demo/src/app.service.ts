import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getHello(): string {
    return '欢迎使用 NestJS 学习演示项目！';
  }

  getHealth(): object {
    return {
      status: 'ok',
      message: '服务运行正常',
      timestamp: new Date().toISOString(),
    };
  }
}
