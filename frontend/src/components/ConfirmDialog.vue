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
      <el-icon class="status-icon warning" v-if="type === 'warning'">
        <WarningFilled/>
      </el-icon>
      <el-icon class="status-icon info" v-else-if="type === 'info'">
        <InfoFilled/>
      </el-icon>
      <div class="message-text">{{ message }}</div>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button class="cancel-btn" @click="$emit('cancel')">{{ cancelText }}</el-button>
        <el-button
            :class="['confirm-btn', confirmButtonType === 'danger' ? 'danger-btn' : 'primary-btn']"
            :type="confirmButtonType"
            @click="$emit('confirm')"
        >
          {{ confirmText }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import {WarningFilled, InfoFilled} from '@element-plus/icons-vue'

defineProps({
  visible: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: '安全确认' // 优化：由原先的“提示”改为更明确的“安全确认”
  },
  message: {
    type: String,
    default: '该操作不可逆，请确认是否继续？' // 优化：提升提示警示力
  },
  width: {
    type: String,
    default: '420px'
  },
  type: {
    type: String,
    default: 'warning' // warning / info
  },
  confirmText: {
    type: String,
    default: '确认继续'
  },
  cancelText: {
    type: String,
    default: '取消'
  },
  confirmButtonType: {
    type: String,
    default: 'danger' // danger / primary
  }
})

defineEmits(['update:visible', 'confirm', 'cancel'])
</script>

<style scoped>
/* 深度自定义 Element Plus 弹窗样式 */
:deep(.custom-confirm-dialog) {
  border-radius: 20px !important;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.25) !important;
  border: 1px solid rgba(203, 213, 225, 0.8);
}

:deep(.el-dialog__header) {
  margin-right: 0;
  padding: 24px 28px 12px;
}

:deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 800;
  color: #020617; /* 更加深邃醒目的黑色 */
  letter-spacing: 0.5px;
}

:deep(.el-dialog__body) {
  padding: 12px 28px 24px;
}

:deep(.el-dialog__footer) {
  padding: 16px 28px 24px;
  border-top: 1px solid #f1f5f9;
  background-color: #f8fafc;
}

/* 弹窗内容排版与强化 */
.dialog-content {
  display: flex;
  align-items: center; /* 顶部对齐，适合多行文本时图标依然美观 */
  gap: 14px;
}

.message-text {
  font-size: 15px;
  font-weight: 600;
  color: #0f172a; /* 加深文案颜色 */
  line-height: 1.6;
  letter-spacing: 0.2px;
  word-break: break-word;
}

/* 状态图标醒目处理 */
.status-icon {
  font-size: 28px;
  flex-shrink: 0;
  margin-top: 2px;
}

.status-icon.warning {
  color: #d97706; /* 加深警告黄 */
  filter: drop-shadow(0 3px 6px rgba(217, 119, 6, 0.3));
}

.status-icon.info {
  color: #0284c7;
  filter: drop-shadow(0 3px 6px rgba(2, 132, 199, 0.3));
}

/* 底部按钮对齐与样式增粗 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

/* 取消按钮 */
.cancel-btn {
  height: 40px;
  border-radius: 12px !important;
  padding: 0 22px;
  font-size: 14px;
  font-weight: 700;
  color: #475569;
  border: 1px solid #cbd5e1;
  background-color: #ffffff;
  transition: all 0.2s ease;
}

.cancel-btn:hover {
  color: #0f172a;
  background-color: #f1f5f9;
  border-color: #94a3b8;
}

/* 危险/确认按钮 (醒目红色渐变) */
.danger-btn {
  height: 40px;
  border-radius: 12px !important;
  padding: 0 22px;
  font-size: 14px;
  font-weight: 700;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
  border: none !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(220, 38, 38, 0.35) !important;
  transition: all 0.25s ease !important;
}

.danger-btn:hover {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%) !important;
  box-shadow: 0 6px 18px rgba(220, 38, 38, 0.45) !important;
}

.danger-btn:active {
  transform: scale(0.97);
}

/* 蓝色确认按钮 (主色调备用) */
.primary-btn {
  height: 40px;
  border-radius: 12px !important;
  padding: 0 22px;
  font-size: 14px;
  font-weight: 700;
  background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important;
  border: none !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35) !important;
  transition: all 0.25s ease !important;
}

.primary-btn:hover {
  background: linear-gradient(135deg, #7dd3fc 0%, #0369a1 100%) !important;
  box-shadow: 0 6px 18px rgba(2, 132, 199, 0.45) !important;
}

.primary-btn:active {
  transform: scale(0.97);
}
</style>