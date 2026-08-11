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
        <el-button class="cancel-btn" @click="$emit('cancel')">{{ cancelText }}</el-button>
        <el-button
            :class="['confirm-btn', confirmButtonType === 'danger' ? 'danger-btn' : 'primary-btn']"
            :type="confirmButtonType"
            @click="$emit('confirm')"
        >
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
/* 深度自定义 Element Plus 弹窗样式 */
:deep(.custom-confirm-dialog) {
  border-radius: 20px !important; /* 统一 20px 大圆角 */
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.18) !important;
  border: 1px solid rgba(226, 232, 240, 0.8);
}

:deep(.el-dialog__header) {
  margin-right: 0;
  padding: 24px 28px 12px;
}

:deep(.el-dialog__title) {
  font-size: 17px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: 0.3px;
}

:deep(.el-dialog__body) {
  padding: 8px 28px 24px;
}

:deep(.el-dialog__footer) {
  padding: 16px 28px 24px;
  border-top: none;
  background-color: #f8fafc; /* 底部背景微对比 */
}

/* 弹窗内容 */
.dialog-content {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: #334155;
  line-height: 1.6;
}

.warning-icon {
  font-size: 26px;
  color: #f59e0b; /* 暖阳黄 */
  flex-shrink: 0;
  filter: drop-shadow(0 2px 4px rgba(245, 158, 11, 0.2));
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* 取消按钮 */
.cancel-btn {
  height: 38px;
  border-radius: 12px !important;
  padding: 0 20px;
  font-weight: 600;
  color: #64748b;
  border: 1px solid #e2e8f0;
  background-color: #ffffff;
  transition: all 0.2s ease;
}

.cancel-btn:hover {
  color: #0f172a;
  background-color: #f1f5f9;
  border-color: #cbd5e1;
}

/* 确认/危险按钮：与 Logo 图红调一致 (#ef4444 ~ #dc2626) */
.danger-btn {
  height: 38px;
  border-radius: 12px !important;
  padding: 0 20px;
  font-weight: 600;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
  border: none !important;
  color: #ffffff !important;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.25) !important;
  transition: all 0.25s ease !important;
}

.danger-btn:hover {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%) !important;
  box-shadow: 0 6px 16px rgba(220, 38, 38, 0.35) !important;
}

.danger-btn:active {
  transform: scale(0.98);
}

/* 极简蓝色按钮（备用） */
.primary-btn {
  height: 38px;
  border-radius: 12px !important;
  padding: 0 20px;
  font-weight: 600;
  background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important;
  border: none !important;
  color: #ffffff !important;
  box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25) !important;
  transition: all 0.25s ease !important;
}

.primary-btn:hover {
  background: linear-gradient(135deg, #7dd3fc 0%, #0369a1 100%) !important;
  box-shadow: 0 6px 16px rgba(2, 132, 199, 0.35) !important;
}

.primary-btn:active {
  transform: scale(0.98);
}
</style>