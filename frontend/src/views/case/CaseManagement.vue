<template>
  <el-card class="content-card" shadow="never">
    <div class="page-header">
      <h3>案件管理中心</h3>
      <p class="page-desc">管理您承办的诉讼、非诉及各类法律顾问案件进展与材料。</p>
    </div>

    <!-- 案件操作栏 -->
    <div class="action-bar">
      <el-button type="primary" size="default">
        <el-icon>
          <Plus/>
        </el-icon>
        新建案件
      </el-button>
    </div>

    <!-- 案件列表表格占位 -->
    <el-table :data="caseList" style="width: 100%; margin-top: 16px;">
      <el-table-column prop="caseNo" label="案号 / 编号" width="180"/>
      <el-table-column prop="title" label="案件名称" min-width="200"/>
      <el-table-column prop="client" label="委托人" width="150"/>
      <el-table-column prop="status" label="当前状态" width="120">
        <template #default="scope">
          <el-tag :type="scope.row.status === '进行中' ? 'success' : 'info'" size="small">
            {{ scope.row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default>
          <el-button link type="primary" size="small">详情</el-button>
          <el-button link type="danger" size="small">归档</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import {ref} from 'vue'
import {Plus} from '@element-plus/icons-vue'

// 模拟一些初始案件数据
const caseList = ref([
  {caseNo: '（2026）京01民初字第1号', title: '某科技公司合同纠纷案', client: '北京XX科技有限公司', status: '进行中'},
  {caseNo: '（2026）京02刑初字第8号', title: '李某某辩护案', client: '李某某家属', status: '进行中'}
])
</script>

<style scoped>
.content-card {
  height: 100%;
  border-radius: 16px !important; /* 延续全局标准圆角 */
  border: 1px solid #e2e8f0 !important;
  background-color: #ffffff !important;
}

.page-header h3 {
  font-size: 18px;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.page-desc {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 16px;
}

.action-bar {
  display: flex;
  justify-content: flex-end;
}
</style>