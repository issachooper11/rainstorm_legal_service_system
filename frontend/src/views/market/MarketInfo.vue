<template>
  <div class="market-container">
    <!-- 1. 顶部搜索与操作卡片 -->
    <el-card class="filter-card" shadow="never" style="margin-bottom: 20px;">
      <el-form :model="queryParams" class="search-form">
        <!-- 第一行输入框：地区、名称、法代 -->
        <div class="form-row">
          <el-form-item label="地区" class="form-item-custom">
            <el-input v-model="queryParams.region" placeholder="请输入地区" clearable @clear="handleQuery"/>
          </el-form-item>
          <el-form-item label="企业名称" class="form-item-custom">
            <el-input v-model="queryParams.enterprise_name" placeholder="请输入企业名称" clearable
                      @clear="handleQuery"/>
          </el-form-item>
          <el-form-item label="法定代表人" class="form-item-custom">
            <el-input v-model="queryParams.legal_representative" placeholder="请输入法定代表人" clearable
                      @clear="handleQuery"/>
          </el-form-item>
        </div>

        <!-- 第二行输入框：电话、邮箱 -->
        <div class="form-row" style="margin-top: 12px;">
          <el-form-item label="联系方式" class="form-item-custom">
            <el-input v-model="queryParams.contact_info" placeholder="请输入联系方式" clearable @clear="handleQuery"/>
          </el-form-item>
          <el-form-item label="邮箱" class="form-item-custom">
            <el-input v-model="queryParams.email" placeholder="请输入邮箱" clearable @clear="handleQuery"/>
          </el-form-item>
        </div>

        <!-- 第三行：类别、意向、签约筛选 -->
        <div class="form-row" style="margin-top: 12px;">
          <el-form-item label="企业类别" class="form-item-custom">
            <el-select v-model="queryParams.enterprise_category" placeholder="全部类别" clearable style="width: 100%;"
                       @change="handleQuery">
              <el-option label="科技" :value="1"/>
              <el-option label="商服" :value="2"/>
              <el-option label="合同" :value="3"/>
              <el-option label="劳动" :value="4"/>
              <el-option label="综合" :value="5"/>
            </el-select>
          </el-form-item>
          <el-form-item label="是否为意向客户" class="form-item-custom">
            <el-select v-model="queryParams.is_intention" placeholder="全部" clearable style="width: 100%;"
                       @change="handleQuery">
              <el-option label="是" :value="true"/>
              <el-option label="否" :value="false"/>
            </el-select>
          </el-form-item>
          <el-form-item label="是否签约" class="form-item-custom">
            <el-select v-model="queryParams.is_signed" placeholder="全部" clearable style="width: 100%;"
                       @change="handleQuery">
              <el-option label="已签约" :value="true"/>
              <el-option label="未签约" :value="false"/>
            </el-select>
          </el-form-item>
        </div>

        <!-- 第四行：按钮操作区 -->
        <div class="form-row action-row">
          <div class="action-right">
            <!-- 批量操作 -->
            <template v-if="isMultiSelect">
              <el-button type="danger" plain @click="handleBatchDelete">
                <el-icon>
                  <Delete/>
                </el-icon>
                <span>批量删除</span>
              </el-button>
              <el-button type="warning" plain @click="handleBatchEmail">
                <el-icon>
                  <Message/>
                </el-icon>
                <span>批量发送邮件</span>
              </el-button>
              <el-button type="success" plain @click="handleBatchSms">
                <el-icon>
                  <Iphone/>
                </el-icon>
                <span>批量发送短信</span>
              </el-button>
              <el-divider direction="vertical" class="action-divider"/>
            </template>

            <!-- 查询与重置 -->
            <el-button type="primary" @click="handleQuery">
              <el-icon>
                <Search/>
              </el-icon>
              <span>查询</span>
            </el-button>
            <el-button @click="resetQuery">
              <el-icon>
                <Refresh/>
              </el-icon>
              <span>重置</span>
            </el-button>

            <el-divider direction="vertical" class="action-divider"/>

            <!-- 上传 Excel 图标按钮 -->
            <el-tooltip content="一键导入 Excel" placement="top">
              <el-upload
                  action="#"
                  :http-request="handleUploadExcel"
                  :show-file-list="false"
                  accept=".xlsx, .xls"
                  class="inline-upload"
              >
                <el-button type="success" circle>
                  <el-icon>
                    <Upload/>
                  </el-icon>
                </el-button>
              </el-upload>
            </el-tooltip>

            <!-- 多选模式开关 -->
            <el-tooltip :content="isMultiSelect ? '关闭多选模式' : '开启多选模式'" placement="top">
              <el-button :type="isMultiSelect ? 'primary' : 'default'" circle @click="toggleMultiSelect">
                <el-icon><Select/></el-icon>
              </el-button>
            </el-tooltip>

            <!-- 操作列显隐开关 -->
            <el-tooltip :content="showOperationCol ? '隐藏操作列' : '显示操作列'" placement="top">
              <el-button :type="showOperationCol ? 'primary' : 'default'" circle
                         @click="showOperationCol = !showOperationCol">
                <el-icon>
                  <Operation/>
                </el-icon>
              </el-button>
            </el-tooltip>
          </div>
        </div>
      </el-form>
    </el-card>

    <!-- 2. 数据表格区域 -->
    <el-card shadow="never">
      <el-table
          v-loading="loading"
          :data="tableData"
          style="width: 100%"
          border
          @sort-change="handleSortChange"
          @selection-change="handleSelectionChange"
      >
        <el-table-column v-if="isMultiSelect" type="selection" width="55" align="center" header-align="center"/>
        <el-table-column type="index" label="序号" min-width="60" align="center" header-align="center"/>

        <!-- 企业类别 -->
        <el-table-column prop="enterprise_category" label="类别" width="80" align="center" header-align="center">
          <template #default="{ row }">
            <el-tag :type="getCategoryType(row.enterprise_category)">
              {{ getCategoryText(row.enterprise_category) }}
            </el-tag>
          </template>
        </el-table-column>

        <!-- 意向客户状态 -->
        <el-table-column label="意向" width="80" align="center" header-align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_intention ? 'success' : 'info'" size="small">
              {{ row.is_intention ? '意向' : '普通' }}
            </el-tag>
          </template>
        </el-table-column>

        <!-- 签约状态 -->
        <el-table-column label="签约" width="80" align="center" header-align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_signed ? 'success' : 'danger'" size="small">
              {{ row.is_signed ? '已签约' : '未签约' }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="region" label="地区" width="80" align="center" header-align="center"/>
        <el-table-column prop="enterprise_name" label="企业名称" min-width="200" show-overflow-tooltip align="center"
                         header-align="center"/>
        <el-table-column prop="legal_representative" label="法定代表人" width="100" align="center"
                         header-align="center"/>

        <!-- 联系方式列 -->
        <el-table-column label="联系方式" min-width="260" align="center" header-align="center">
          <template #default="{ row }">
            <div v-if="row.contact_info && row.contact_info.length" class="cell-list-container">
              <div v-for="(item, index) in row.contact_info" :key="index" class="json-cell-item">
                <span
                    :class="['status-text', item.is_sms_sent ? 'is-sent' : 'is-pending']"
                    @click="handleSendMsg('sms', row, item, index)"
                >
                  【{{ item.is_sms_sent ? '已发送' : '待发送' }}】
                </span>
                <span>{{ item.phone }}：{{ item.name || '待查询' }}</span>
              </div>
            </div>
            <span v-else style="color: #909399;">暂无联系方式</span>
          </template>
        </el-table-column>

        <!-- 邮箱列 -->
        <el-table-column label="邮箱" min-width="240" align="center" header-align="center">
          <template #default="{ row }">
            <div v-if="row.email && row.email.length" class="cell-list-container">
              <div v-for="(item, index) in row.email" :key="index" class="json-cell-item">
                <span
                    :class="['status-text', item.is_sent ? 'is-sent' : 'is-pending']"
                    @click="handleSendMsg('email', row, item, index)"
                >
                  【{{ item.is_sent ? '已发送' : '待发送' }}】
                </span>
                <span>{{ item.email }}</span>
              </div>
            </div>
            <span v-else style="color: #909399;">暂无邮箱</span>
          </template>
        </el-table-column>

        <!-- 成立日期排序 -->
        <el-table-column prop="establishment_date" label="成立日期" width="110" sortable="custom" align="center"
                         header-align="center"/>

        <!-- 注册资本排序 -->
        <el-table-column prop="registered_capital" label="注册资本" width="130" sortable="custom" align="center"
                         header-align="center">
          <template #default="{ row }">
            <span>{{ row.registered_capital ? row.registered_capital + ' 万元' : '暂无' }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="enterprise_type" label="企业类型" min-width="150" align="left" show-overflow-tooltip
                         header-align="center"/>
        <el-table-column prop="registered_address" label="注册地址" min-width="180" align="left" show-overflow-tooltip
                         header-align="center"/>

        <!-- 操作列 -->
        <el-table-column
            v-if="showOperationCol"
            label="操作"
            width="180"
            fixed="right"
            align="center"
            header-align="center"
        >
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleOpenTrace(row)">跟进</el-button>
            <el-button type="warning" link size="small" @click="handleEdit(row)">修改</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 3. 分页组件 -->
      <div class="pagination-container" style="margin-top: 20px; display: flex; justify-content: flex-end;">
        <el-pagination
            v-model:current-page="queryParams.page"
            v-model:page-size="queryParams.page_size"
            :page-sizes="[5, 10, 25, 50]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 4. 修改企业信息对话框 -->
    <el-dialog v-model="editDialogVisible" title="修改企业信息" width="650px" destroy-on-close>
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="企业名称">
          <el-input v-model="editForm.enterprise_name" disabled placeholder="企业名称不可修改"/>
        </el-form-item>
        <el-form-item label="地区">
          <el-input v-model="editForm.region" disabled placeholder="请输入地区"/>
        </el-form-item>
        <el-form-item label="法定代表人">
          <el-input v-model="editForm.legal_representative" disabled placeholder="请输入法定代表人"/>
        </el-form-item>
        <el-form-item label="企业类别">
          <el-select v-model="editForm.enterprise_category" placeholder="请选择企业类别" style="width: 100%;">
            <el-option label="科技" :value="1"/>
            <el-option label="商服" :value="2"/>
            <el-option label="合同" :value="3"/>
            <el-option label="劳动" :value="4"/>
            <el-option label="综合" :value="5"/>
          </el-select>
        </el-form-item>
        <el-form-item label="意向/签约">
          <el-checkbox v-model="editForm.is_intention">设为意向客户</el-checkbox>
          <el-checkbox v-model="editForm.is_signed">已签约客户</el-checkbox>
        </el-form-item>

        <!-- 动态编辑联系人列表 -->
        <el-form-item label="联系方式">
          <div v-for="(item, index) in editForm.contact_info" :key="index" class="edit-row-item">
            <el-input v-model="item.name" placeholder="姓名" style="width: 100px; margin-right: 8px;"/>
            <el-input v-model="item.phone" placeholder="电话号码" style="width: 160px; margin-right: 8px;"/>
            <el-checkbox v-model="item.is_sms_sent" style="margin-right: 8px;">已发短信</el-checkbox>
            <el-button type="danger" circle icon="Delete" size="small" @click="removeContact(index)"/>
          </div>
          <div class="add-btn-wrapper">
            <el-button type="primary" plain size="small" icon="Plus" @click="addContact">添加号码</el-button>
          </div>
        </el-form-item>

        <!-- 动态编辑邮箱列表 -->
        <el-form-item label="邮箱">
          <div v-for="(item, index) in editForm.email" :key="index" class="edit-row-item">
            <el-input v-model="item.email" placeholder="邮箱地址" style="width: 240px; margin-right: 8px;"/>
            <el-checkbox v-model="item.is_sent" style="margin-right: 8px;">已发邮件</el-checkbox>
            <el-button type="danger" circle icon="Delete" size="small" @click="removeEmail(index)"/>
          </div>
          <div class="add-btn-wrapper">
            <el-button type="primary" plain size="small" icon="Plus" @click="addEmail">添加邮箱</el-button>
          </div>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="editSubmitting" @click="submitEdit">保存</el-button>
      </template>
    </el-dialog>

    <!-- 5. 跟进记录侧边抽屉 -->
    <el-drawer
        v-model="traceDrawerVisible"
        :title="`跟进记录 -- ${currentEnterprise.enterprise_name || ''}`"
        size="520px"
        direction="rtl"
        custom-class="custom-trace-drawer"
    >
      <div class="drawer-inner-container">
        <!-- 5.1 添加跟进卡片 -->
        <div class="trace-card add-card">
          <div class="card-header">
            <span class="header-mark"></span>
            <span class="header-title">添加新跟进</span>
          </div>
          <el-form :model="traceForm" label-width="80px" label-position="left" class="trace-form">
            <el-form-item label="跟进方式">
              <el-select v-model="traceForm.trace_type" placeholder="请选择跟进方式" style="width: 100%;">
                <el-option label="邮件" :value="1"/>
                <el-option label="电话" :value="2"/>
                <el-option label="微信" :value="3"/>
                <el-option label="线下" :value="4"/>
              </el-select>
            </el-form-item>
            <el-form-item label="跟进内容">
              <el-input
                  v-model="traceForm.content"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入本次沟通详情、客户反馈等..."
                  resize="none"
              />
            </el-form-item>
            <div class="form-action-right">
              <el-button type="primary" class="submit-btn" :loading="traceSubmitting" @click="submitTrace">
                提交跟进
              </el-button>
            </div>
          </el-form>
        </div>

        <!-- 5.2 历史跟进轨迹卡片列表 -->
        <div class="trace-card history-card">
          <div class="card-header">
            <span class="header-mark"></span>
            <span class="header-title">历史跟进轨迹</span>
          </div>

          <div v-if="traceList.length === 0" class="empty-trace">
            <el-empty description="暂无跟进记录" :image-size="80"/>
          </div>

          <div v-else class="timeline-scroll-container">
            <div v-for="item in traceList" :key="item.id" class="history-item-card">
              <div class="item-header">
                <div class="header-left">
                  <el-tag size="small" class="type-tag" :type="getTraceTypeTag(item.trace_type)">
                    {{ getTraceTypeText(item.trace_type) }}
                  </el-tag>
                  <span class="creator-name">跟进人：{{ item.creator_name || '系统用户' }}</span>
                </div>
                <span class="trace-time">{{ formatDate(item.created_at) }}</span>
              </div>
              <div class="item-body">
                <p class="trace-content">{{ item.content }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-drawer>

    <!-- 6. 短信发送弹窗 -->
    <el-dialog
        v-model="smsDialogVisible"
        title="发送营销短信"
        width="500px"
        destroy-on-close
    >
      <el-form :model="smsForm" label-width="90px">
        <el-form-item label="接收手机">
          <el-input v-model="smsForm.phone" disabled/>
        </el-form-item>
        <el-form-item label="接收人">
          <el-input v-model="smsForm.name" disabled/>
        </el-form-item>
        <el-form-item label="企业类别">
          <el-select
              v-model="smsForm.category"
              placeholder="请选择类别"
              style="width: 100%;"
              @change="handleSmsCategoryChange"
          >
            <el-option label="科技" :value="1"/>
            <el-option label="商服" :value="2"/>
            <el-option label="合同" :value="3"/>
            <el-option label="劳动" :value="4"/>
            <el-option label="综合" :value="5"/>
          </el-select>
        </el-form-item>
        <el-form-item label="短信内容">
          <el-input
              v-model="smsForm.content"
              type="textarea"
              :rows="4"
              readonly
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="smsDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="smsSending" @click="submitSendSms">确定发送</el-button>
      </template>
    </el-dialog>

    <!-- 7. 邮箱发送弹窗（已去除海报附件行） -->
    <el-dialog
        v-model="emailDialogVisible"
        title="发送营销邮件"
        width="580px"
        destroy-on-close
    >
      <el-form :model="emailForm" label-width="90px">
        <el-form-item label="接收邮箱">
          <el-input v-model="emailForm.email" disabled/>
        </el-form-item>
        <el-form-item label="企业类别">
          <el-select
              v-model="emailForm.category"
              placeholder="请选择企业类别"
              style="width: 100%;"
              @change="handleEmailCategoryChange"
          >
            <el-option label="科技" :value="1"/>
            <el-option label="商服" :value="2"/>
            <el-option label="合同" :value="3"/>
            <el-option label="劳动" :value="4"/>
            <el-option label="综合" :value="5"/>
          </el-select>
        </el-form-item>
        <el-form-item label="邮件主题">
          <el-input v-model="emailForm.subject" readonly/>
        </el-form-item>
        <el-form-item label="正文预览">
          <el-input
              v-model="emailForm.body"
              type="textarea"
              :rows="6"
              readonly
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="emailDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="emailSending" @click="submitSendEmail">确定发送</el-button>
      </template>
    </el-dialog>

    <!-- 8. 通用 ConfirmDialog 确认弹窗 -->
    <ConfirmDialog
        v-model:visible="confirmDialogVisible"
        :title="confirmDialogTitle"
        :message="confirmDialogMessage"
        :type="confirmDialogType"
        :confirm-button-type="confirmButtonType"
        @confirm="handleConfirmAction"
        @cancel="confirmDialogVisible = false"
    />
  </div>
</template>

<script setup>
import {ref, reactive, onMounted} from 'vue'
import {ElMessage} from 'element-plus'
import {Upload, Operation, Select, Search, Refresh, Delete, Message, Iphone, Plus} from '@element-plus/icons-vue'

import {
  getMarketListApi,
  importMarketExcelApi,
  updateMarketApi,
  deleteMarketApi,
  sendMarketEmailApi
} from "../../api/market.js"
import {getEnterpriseTracesApi, createEnterpriseTraceApi} from "../../api/trace.js"
import ConfirmDialog from "../../components/ConfirmDialog.vue";

// ---------------- 1. 营销模板数据常量定义 ----------------
const EMAIL_TEMPLATES = {
  1: {
    subject: "【法律体检】企业的五维法律风险排查清单",
    body: `{company_name} 负责人：

您好！

企业的风控，从来不是赢得一场官司，而是在源头规避掉不必要的麻烦。

我们把企业在公司治理、合同履约、财税合规、劳动用工以及知产数据中最容易踩坑的风险点，梳理成了下方这份 《企业法律健康体检清单》。

建议您花 2 分钟对照自查。如果发现有不确定或存在隐患的地方：

1、直接回复本邮件；

2、或 扫描下方二维码 / 添加微信 (15810733362)。

我们常法团队将为您提供 1 次 15 分钟的线上免费解读，帮您把把脉，提前消除风险隐患。

顺祝商祺！

北京觅理律师事务所 常法团队`
  },

  2: {
    subject: "【商服企业防坑】服务回款、履约边界与账期风险排查",
    body: `尊敬的 {company_name} ：

您好！

商业服务型企业高频交易多、账期长，在日常经营中极易踩中以下隐患：
• 【坏账与回款难题】：服务成果已交付，客户却借故拖欠尾款或无限期压账；
• 【履约边界模糊】：服务合同未设置阶段性验收标准，导致客户无休止要求免费修改；
• 【财税合规隐患】：公私户划转、无票支出或发票开具时点不当，诱发补税及罚款风险。

针对商服企业的经营特性，北京觅理律师事务所常法团队特别整理了《企业法律健康体检清单》（随信附于下方），帮您快速梳理合同与账款安全。

🎁 专属服务：
回复本邮件或添加微信（15810733362），即可免费领取《企业合规全周期防护手册》，并预约 1 次 15 分钟资深律师线上免费风险诊断。`
  },

  3: {
    subject: "【合同与交易合规】质量检验、履约留痕与发票风险排查",
    body: `尊敬的 {company_name} ：

您好！

交易合同是企业的生命线，上下游合作中的细节漏洞往往会给企业造成巨额损失：
• 【合同订立漏洞】：未明确“质量异议期”与交付标准，买方以质量瑕疵为由拒付货款；
• 【举证防线缺失】：微信、邮件等关键沟通记录未规范留痕，发生纠纷时举证困难；
• 【发票合规风险】：进项发票开具不及时或真实性核查不到位，引发税务稽查风险。

为帮助贵司筑牢交易防火墙，北京觅理律师事务所常法团队特别整理了《企业法律健康体检清单》（随信附于下方），方便您 1 分钟快速自查。

🎁 专属服务：
若您想了解如何建立标准化的合同审核流程，直接回复本邮件或添加微信（15810733362），即可预约资深律师 15 分钟免费线上咨询。`
  },

  4: {
    subject: "【劳动用工预警】社保新规、试用期辞退与 2N 赔偿避坑指南",
    body: `尊敬的 {company_name} ：

您好！

劳动用工是企业最易发生诉讼的重灾区，尤其是随着社保与劳动法规趋严，企业需高度警惕：
• 【社保合规新规】：任何“自愿放弃社保协议”均属无效！未足额缴纳社保，员工可随时解约并索赔；
• 【试用期辞退风险】：缺乏明确的录用条件与考核证据，试用期辞退极易被判违法解除（2N 赔偿）；
• 【加班与考勤漏洞】：考勤制度未依法公示或加班费留痕不规范，离职时面临追讨风险。

北京觅理律师事务所常法团队梳理了最新的《企业法律健康体检清单》（随信附于下方），帮您排查用工隐患。

🎁 专属服务：
直接回复本邮件，或添加微信（15810733362），即可免费获取《企业用工合规全套制度模板》，并享受 15 分钟线上免费法律咨询。`
  },

  5: {
    subject: "【企业全维合规】新《公司法》应对、合同与用工风险排查",
    body: `尊敬的 {company_name} ：

您好！

新《公司法》全面实施背景下，资本实缴与股东责任追溯趋严。企业日常经营若缺乏常态化合规排查，极易产生系统性风险：
• 【公司治理】：章程照搬互联网模板，注册资本未规划 5 年实缴路径，公私户混用；
• 【劳动用工】：劳动合同未及时续签、试用期考核缺乏留痕、社保缴纳不规范；
• 【合同防线】：标准合同条款失衡、公章管理不严格、账期追偿缺乏法律保障。

北京觅理律师事务所常法团队将复杂的法律条款提炼为《企业法律健康体检清单》（随信附于下方），方便您快速评估企业合规健康度。

🎁 专属服务：
直接回复本邮件或微信联系（15810733362），即可预约觅理律所资深团队为您提供 1 次 15 分钟线上免费法律健康诊断。`
  }
}

const SMS_TEMPLATES = {
  1: "【觅理律所】尊敬的{company_name}负责人：新公司法下股权退出与知产泄密风险高发！已为您准备1份《科技企业法律自查清单》，回复1免费领电子版及15分钟资深律师解读。回T退订",
  2: "【觅理律所】尊敬的{company_name}负责人：服务成果已交付尾款却被拖欠？已为您整理《商服企业坏账与合同防坑清单》，回复1免费领取及15分钟资深律师解读。回T退订",
  3: "【觅理律所】尊敬的{company_name}负责人：合同条款漏洞易致货款难追！已为您整理《企业合同与交易合规自查表》，回复1免费领取及15分钟资深律师线上评估。回T退订",
  4: "【觅理律所】尊敬的{company_name}负责人：试用期辞退与社保补缴易引发巨额索赔！已为您准备《用工合规与避坑清单》，回复1免费领全套制度模板及律师咨询。回T退订",
  5: "【觅理律所】尊敬的{company_name}负责人：新公司法实施，5年实缴与用工风险如何排查？已为您准备《企业法律健康体检清单》，回复1免费领取资深律师解读。回T退订"
}

const formatDate = (isoString) => {
  if (!isoString) return ''
  return isoString.replace('T', ' ').split('.')[0]
}

// ---------------- 2. 状态与变量定义 ----------------
const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const showOperationCol = ref(true)
const isMultiSelect = ref(false)
const selectedRows = ref([])

const queryParams = reactive({
  region: '',
  enterprise_name: '',
  legal_representative: '',
  contact_info: '',
  email: '',
  enterprise_category: undefined,
  is_intention: undefined,
  is_signed: undefined,
  sort_field: '',
  sort_order: 'asc',
  page: 1,
  page_size: 10
})

// 修改对话框状态与表单
const editDialogVisible = ref(false)
const editSubmitting = ref(false)
const currentEditId = ref(null)
const editForm = reactive({
  enterprise_name: '',
  region: '',
  legal_representative: '',
  enterprise_category: 5,
  is_intention: false,
  is_signed: false,
  contact_info: [],
  email: []
})

// 抽屉跟进状态
const traceDrawerVisible = ref(false)
const currentEnterprise = ref({})
const traceList = ref([])
const traceSubmitting = ref(false)
const traceForm = reactive({trace_type: 2, content: ''})

// 发送目标与弹窗状态
const currentTargetRow = ref(null)
const currentTargetItem = ref(null)

// 短信弹窗
const smsDialogVisible = ref(false)
const smsSending = ref(false)
const smsForm = reactive({
  phone: '',
  name: '',
  category: 5,
  content: ''
})

// 邮箱弹窗
const emailDialogVisible = ref(false)
const emailSending = ref(false)
const emailForm = reactive({
  email: '',
  category: 5,
  subject: '',
  body: ''
})

// ConfirmDialog 状态管理
const confirmDialogVisible = ref(false)
const confirmDialogTitle = ref('警告')
const confirmDialogMessage = ref('')
const confirmDialogType = ref('warning')
const confirmButtonType = ref('danger')
const currentActionType = ref('') // 'singleDelete' | 'batchDelete'
const rowToDelete = ref(null)

// ---------------- 3. 方法分发入口 ----------------
const handleSendMsg = (type, row, item) => {
  currentTargetRow.value = row
  currentTargetItem.value = item

  if (type === 'sms') {
    if (item.is_sms_sent) {
      ElMessage.info(`短信已发送给：${item.phone}`)
      return
    }
    smsForm.phone = item.phone
    smsForm.name = item.name || '待查询'
    smsForm.category = row.enterprise_category || 5

    handleSmsCategoryChange(smsForm.category)
    smsDialogVisible.value = true

  } else if (type === 'email') {
    if (item.is_sent) {
      ElMessage.info(`邮件已发送给：${item.email}`)
      return
    }
    emailForm.email = item.email
    emailForm.category = row.enterprise_category || 5

    handleEmailCategoryChange(emailForm.category)
    emailDialogVisible.value = true
  }
}

// ---------------- 4. 短信弹窗逻辑 ----------------
const handleSmsCategoryChange = (catVal) => {
  const companyName = currentTargetRow.value?.enterprise_name || ''
  const tpl = SMS_TEMPLATES[catVal] || SMS_TEMPLATES[5]
  smsForm.content = tpl.replace('{company_name}', companyName)
}

const submitSendSms = async () => {
  smsSending.value = true
  try {
    const updatedContactInfo = JSON.parse(JSON.stringify(currentTargetRow.value.contact_info || []))
    const target = updatedContactInfo.find(c => c.phone === currentTargetItem.value.phone)
    if (target) {
      target.is_sms_sent = true
    }

    await updateMarketApi(currentTargetRow.value.id, {
      ...currentTargetRow.value,
      contact_info: updatedContactInfo
    })

    currentTargetItem.value.is_sms_sent = true
    ElMessage.success('短信发送成功，状态已更新！')
    smsDialogVisible.value = false
  } catch (error) {
    console.error('发送短信失败:', error)
    ElMessage.error('短信发送失败')
  } finally {
    smsSending.value = false
  }
}

// ---------------- 5. 邮箱弹窗逻辑 ----------------
const handleEmailCategoryChange = (catVal) => {
  const companyName = currentTargetRow.value?.enterprise_name || ''
  const tpl = EMAIL_TEMPLATES[catVal] || EMAIL_TEMPLATES[5]

  emailForm.subject = tpl.subject
  emailForm.body = tpl.body.replace('{company_name}', companyName)
}

const submitSendEmail = async () => {
  emailSending.value = true
  try {
    await sendMarketEmailApi({
      enterprise_id: Number(currentTargetRow.value.id),
      email: String(emailForm.email).trim(),
      subject: emailForm.subject,
      body: emailForm.body
    })

    const updatedEmailList = JSON.parse(JSON.stringify(currentTargetRow.value.email || []))
    const target = updatedEmailList.find(e => e.email === currentTargetItem.value.email)
    if (target) {
      target.is_sent = true
    }

    await updateMarketApi(currentTargetRow.value.id, {
      ...currentTargetRow.value,
      email: updatedEmailList
    })

    currentTargetItem.value.is_sent = true
    ElMessage.success('邮件已成功发送！')
    emailDialogVisible.value = false
  } catch (error) {
    console.error('发送邮件失败:', error)
    ElMessage.error(error.response?.data?.detail?.[0]?.msg || '邮件发送失败，请检查数据格式')
  } finally {
    emailSending.value = false
  }
}

// ---------------- 6. 数据表格与筛选逻辑 ----------------
const fetchTableData = async () => {
  loading.value = true
  try {
    const res = await getMarketListApi(queryParams)
    if (res) {
      tableData.value = res.items
      total.value = res.total
    }
  } catch (error) {
    console.error('获取市场信息失败', error)
    ElMessage.error('获取数据失败，请检查网络或后端服务')
  } finally {
    loading.value = false
  }
}

const handleQuery = () => {
  queryParams.page = 1
  fetchTableData()
}

const resetQuery = () => {
  queryParams.region = ''
  queryParams.enterprise_name = ''
  queryParams.legal_representative = ''
  queryParams.contact_info = ''
  queryParams.email = ''
  queryParams.enterprise_category = undefined
  queryParams.is_intention = undefined
  queryParams.is_signed = undefined
  queryParams.sort_field = ''
  queryParams.sort_order = 'asc'
  queryParams.page = 1
  queryParams.page_size = 10
  fetchTableData()
}

// ---------------- 7. 编辑企业逻辑 ----------------
const handleEdit = (row) => {
  currentEditId.value = row.id
  editForm.enterprise_name = row.enterprise_name
  editForm.region = row.region
  editForm.legal_representative = row.legal_representative
  editForm.enterprise_category = row.enterprise_category || 5
  editForm.is_intention = row.is_intention || false
  editForm.is_signed = row.is_signed || false
  editForm.contact_info = JSON.parse(JSON.stringify(row.contact_info || []))
  editForm.email = JSON.parse(JSON.stringify(row.email || []))
  editDialogVisible.value = true
}

const addContact = () => {
  editForm.contact_info.push({name: '待查询', phone: '', is_sms_sent: false})
}

const removeContact = (index) => {
  editForm.contact_info.splice(index, 1)
}

const addEmail = () => {
  editForm.email.push({email: '', is_sent: false})
}

const removeEmail = (index) => {
  editForm.email.splice(index, 1)
}

const submitEdit = async () => {
  editSubmitting.value = true
  try {
    await updateMarketApi(currentEditId.value, editForm)
    ElMessage.success('企业信息修改成功')
    editDialogVisible.value = false
    fetchTableData()
  } catch (error) {
    console.error('修改失败', error)
    ElMessage.error('修改失败，请重试')
  } finally {
    editSubmitting.value = false
  }
}

// ---------------- 8. 删除与批量处理 (已改用 ConfirmDialog) ----------------
const handleDelete = (row) => {
  rowToDelete.value = row
  currentActionType.value = 'singleDelete'
  confirmDialogTitle.value = '警告'
  confirmDialogMessage.value = `确认要删除企业【${row.enterprise_name}】吗？`
  confirmDialogType.value = 'warning'
  confirmButtonType.value = 'danger'
  confirmDialogVisible.value = true
}

const handleBatchDelete = () => {
  if (selectedRows.value.length === 0) return ElMessage.warning('请先勾选需要批量删除的项')
  currentActionType.value = 'batchDelete'
  confirmDialogTitle.value = '批量删除确认'
  confirmDialogMessage.value = `确认要删除选中的 ${selectedRows.value.length} 项数据吗？`
  confirmDialogType.value = 'warning'
  confirmButtonType.value = 'danger'
  confirmDialogVisible.value = true
}

// ConfirmDialog 统一点击确认后的响应函数
const handleConfirmAction = async () => {
  confirmDialogVisible.value = false
  if (currentActionType.value === 'singleDelete') {
    try {
      await deleteMarketApi(rowToDelete.value.id)
      ElMessage.success('删除成功')
      fetchTableData()
    } catch (error) {
      ElMessage.error('删除失败')
    } finally {
      rowToDelete.value = null
    }
  } else if (currentActionType.value === 'batchDelete') {
    // 处理批量删除 API 调用逻辑
    ElMessage.info(`已触发删除 ${selectedRows.value.length} 项`)
  }
}

const handleSelectionChange = (val) => {
  selectedRows.value = val
}

const toggleMultiSelect = () => {
  isMultiSelect.value = !isMultiSelect.value
  if (!isMultiSelect.value) selectedRows.value = []
}

const handleBatchEmail = () => {
  if (selectedRows.value.length === 0) return ElMessage.warning('请先勾选需要发送邮件的项')
  ElMessage.info(`已选择 ${selectedRows.value.length} 项，触发批量发邮件`)
}

const handleBatchSms = () => {
  if (selectedRows.value.length === 0) return ElMessage.warning('请先勾选需要发送短信的项')
  ElMessage.info(`已选择 ${selectedRows.value.length} 项，触发批量发短信`)
}

const handleSortChange = ({prop, order}) => {
  queryParams.sort_field = order ? prop : ''
  queryParams.sort_order = order === 'ascending' ? 'asc' : 'desc'
  fetchTableData()
}

const handleSizeChange = (val) => {
  queryParams.page_size = val
  fetchTableData()
}

const handleCurrentChange = (val) => {
  queryParams.page = val
  fetchTableData()
}

// ---------------- 9. 跟进记录逻辑 ----------------
const handleOpenTrace = async (row) => {
  currentEnterprise.value = row
  traceForm.content = '发送邮件，确认手机号和微信'
  traceForm.trace_type = 1
  traceDrawerVisible.value = true
  await fetchTraces(row.id)
}

const fetchTraces = async (enterpriseId) => {
  try {
    const res = await getEnterpriseTracesApi(enterpriseId)
    if (res) traceList.value = res
  } catch (error) {
    ElMessage.error('获取跟进记录失败')
  }
}

const submitTrace = async () => {
  if (!traceForm.content.trim()) return ElMessage.warning('请输入跟进详细内容')
  traceSubmitting.value = true
  try {
    await createEnterpriseTraceApi(currentEnterprise.value.id, {
      trace_type: traceForm.trace_type,
      content: traceForm.content
    })
    ElMessage.success('跟进记录添加成功')
    traceForm.content = ''
    await fetchTraces(currentEnterprise.value.id)
  } catch (error) {
    ElMessage.error('添加失败')
  } finally {
    traceSubmitting.value = false
  }
}

// ---------------- 10. Excel 导入与工具函数 ----------------
const handleUploadExcel = async (options) => {
  try {
    const res = await importMarketExcelApi(options.file)
    if (res && res.code === 200) {
      ElMessage.success({message: `导入完成！成功新增 ${res.data.success_count} 条数据。`, duration: 5000})
      fetchTableData()
    }
  } catch (error) {
    ElMessage.error('Excel 导入失败')
  }
}

const getCategoryType = (c) => ({1: 'success', 2: 'warning', 3: 'primary', 4: 'danger', 5: 'info'}[c] || 'info')
const getCategoryText = (c) => ({1: '科技', 2: '商服', 3: '合同', 4: '劳动', 5: '综合'}[c] || '未知')
const getTraceTypeTag = (t) => ({1: 'info', 2: 'success', 3: 'warning', 4: 'danger'}[t] || '')
const getTraceTypeText = (t) => ({1: '邮件', 2: '电话', 3: '微信', 4: '线下'}[t] || '未知')

onMounted(() => {
  fetchTableData()
})
</script>

<style scoped>
.search-form {
  width: 100%;
}

.form-row {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
}

.action-row {
  margin-top: 16px;
  justify-content: flex-end;
}

.form-item-custom {
  flex: 1;
  margin: 0 !important;
}

.form-item-custom :deep(.el-form-item__content) {
  width: 100%;
}

.form-item-custom :deep(.el-input),
.form-item-custom :deep(.el-select) {
  width: 100% !important;
}

.action-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.action-right .el-button {
  margin: 0 !important;
}

.action-divider {
  margin: 0 4px;
  height: 18px;
}

.inline-upload {
  display: inline-flex;
  align-items: center;
}

.cell-list-container {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 4px 0;
}

.json-cell-item {
  display: flex;
  align-items: center;
  justify-content: left;
  font-size: 13px;
  line-height: 1.6;
}

.edit-row-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  width: 100%;
}

.add-btn-wrapper {
  width: 100%;
  display: flex;
  justify-content: flex-start;
  margin-top: 4px;
}

.timeline-scroll-container {
  max-height: 50vh;
  overflow-y: auto;
  padding-right: 8px;
}

.timeline-scroll-container::-webkit-scrollbar {
  width: 6px;
}

.timeline-scroll-container::-webkit-scrollbar-thumb {
  background-color: #dcdfe6;
  border-radius: 3px;
}

.status-text {
  cursor: pointer;
  font-weight: 500;
  margin-right: 4px;
  user-select: none;
  transition: opacity 0.2s;
}

.status-text:hover {
  opacity: 0.8;
}

.status-text.is-pending {
  color: #e6a23c;
}

.status-text.is-sent {
  color: #67c23a;
}

/* ==================== 跟进记录抽屉专项优化样式 ==================== */
/* 抽屉整体间距与背景 */
.drawer-inner-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 4px;
}

/* 通用区块卡片样式（与 20px 圆角保持一致） */
.trace-card {
  background-color: #ffffff;
  border-radius: 16px;
  border: 1px solid rgba(226, 232, 240, 0.8);
  padding: 18px 20px;
  box-shadow: 0 4px 12px -2px rgba(15, 23, 42, 0.05);
  transition: all 0.2s ease;
}

/* 卡片标题及标志线条 */
.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.header-mark {
  width: 4px;
  height: 16px;
  background-color: #0284c7;
  border-radius: 2px;
}

.header-title {
  font-size: 16px;
  font-weight: 800;
  color: #020617; /* 深度加黑，醒目突出 */
  letter-spacing: 0.3px;
}

/* 表单内部对齐与按钮控制 */
.trace-form :deep(.el-form-item__label) {
  font-weight: 700;
  color: #1e293b; /* 标签文字加深 */
}

.trace-form :deep(.el-textarea__inner) {
  border-radius: 8px;
  color: #0f172a;
}

.form-action-right {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
}

.submit-btn {
  height: 40px; /* 根据需要调整高度 */
  border-radius: 10px;
  font-weight: 600;
  padding: 0 20px;
}

/* 历史列表滚动容器 */
.timeline-scroll-container {
  max-height: calc(100vh - 380px);
  overflow-y: auto;
  padding-right: 6px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.timeline-scroll-container::-webkit-scrollbar {
  width: 5px;
}

.timeline-scroll-container::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 4px;
}

/* 历史单条记录卡片 */
.history-item-card {
  background-color: #f8fafc;
  border: 1px solid #f1f5f9;
  border-radius: 12px;
  padding: 12px 14px;
  transition: all 0.2s ease;
}

.history-item-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.04);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.type-tag {
  font-weight: 700;
  border-radius: 6px;
}

.creator-name {
  font-size: 13px;
  font-weight: 700;
  color: #334155; /* 文字加深对齐 */
}

.trace-time {
  font-size: 12px;
  color: #64748b;
}

.item-body {
  padding-top: 2px;
}

.trace-content {
  margin: 0;
  font-size: 14px;
  color: #0f172a; /* 正文文字深度加黑 */
  line-height: 1.55;
  white-space: pre-wrap;
  word-break: break-all;
}

.empty-trace {
  padding: 20px 0;
}
</style>