<template>
  <el-dialog
      :model-value="visible"
      @update:model-value="$emit('update:visible', $event)"
      :title="title"
      :width="width"
      align-center
      class="custom-confirm-dialog"
      @close="$emit('cancel')"
  >
    <div class="dialog-content">
      <el-icon class="warning-icon" v-if="type === 'warning'">
        <WarningFilled/>
      </el-icon>
      <span>{{ message }}</span>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="$emit('cancel')">{{ cancelText }}</el-button>
        <el-button :type="confirmButtonType" @click="$emit('confirm')">
          {{ confirmText }}
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import {WarningFilled} from '@element-plus/icons-vue'

defineProps({
  visible: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: '提示'
  },
  message: {
    type: String,
    default: '确认进行此操作吗？'
  },
  width: {
    type: String,
    default: '400px'
  },
  type: {
    type: String,
    default: 'warning' // warning / info
  },
  confirmText: {
    type: String,
    default: '确定'
  },
  cancelText: {
    type: String,
    default: '取消'
  },
  confirmButtonType: {
    type: String,
    default: 'danger' // 退出通常用危险红色按钮
  }
})

defineEmits(['update:visible', 'confirm', 'cancel'])
</script>

<style scoped>
/* 深度自定义 Element Plus 弹窗样式，保持现代圆角与扁平化风格 */
:deep(.custom-confirm-dialog) {
  border-radius: 12px; /* 统一圆角，与登录卡片风格一致 */
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

:deep(.el-dialog__header) {
  margin-right: 0;
  padding: 20px 24px 10px;
  font-weight: 600;
}

:deep(.el-dialog__body) {
  padding: 10px 24px 20px;
}

:deep(.el-dialog__footer) {
  padding: 10px 24px 20px;
  border-top: none;
}

.dialog-content {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 15px;
  color: #334155;
}

.warning-icon {
  font-size: 24px;
  color: #eab308; /* 警告黄 */
  flex-shrink: 0;
}
</style>