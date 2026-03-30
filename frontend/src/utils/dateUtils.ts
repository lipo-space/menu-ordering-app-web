/**
 * 日期时间工具函数 - 确保使用北京时间（UTC+8）
 */

/**
 * 格式化日期为北京时间
 */
export function formatDateBeijing(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
}

/**
 * 格式化时间为北京时间（小时:分钟）
 */
export function formatTimeBeijing(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleTimeString('zh-CN', {
    timeZone: 'Asia/Shanghai',
    hour: '2-digit',
    minute: '2-digit'
  })
}

/**
 * 格式化完整日期时间为北京时间
 */
export function formatDateTimeBeijing(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long',
    hour: '2-digit',
    minute: '2-digit'
  })
}

/**
 * 从指定日期获取北京时间日期（YYYY-MM-DD格式）
 */
function getBeijingDateFrom(date: Date): string {
  const beijingTime = new Date(date.toLocaleString('en-US', { timeZone: 'Asia/Shanghai' }))
  const year = beijingTime.getFullYear()
  const month = String(beijingTime.getMonth() + 1).padStart(2, '0')
  const day = String(beijingTime.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

/**
 * 获取当前北京时间日期（YYYY-MM-DD格式）
 */
export function getTodayBeijing(): string {
  return getBeijingDateFrom(new Date())
}

/**
 * 检查给定日期是否为北京时间今天
 */
export function isTodayBeijing(dateString: string): boolean {
  const dateStr = dateString.split('T')[0] // 确保只比较日期部分
  const todayStr = getTodayBeijing()
  return dateStr === todayStr
}

/**
 * 获取N天前的北京时间日期（YYYY-MM-DD格式）
 */
export function getDaysAgoBeijing(days: number): string {
  const date = new Date(Date.now() - days * 24 * 60 * 60 * 1000)
  return getBeijingDateFrom(date)
}
