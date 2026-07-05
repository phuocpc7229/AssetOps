const DATE_PATTERN = /^(\d{2})\/(\d{2})\/(\d{4})$/

export const isoToDisplayDate = (value: string | null) => {
  if (!value) {
    return ''
  }

  const [year, month, day] = value.split('-')
  if (!year || !month || !day) {
    return ''
  }

  return `${day}/${month}/${year}`
}

export const displayDateToIso = (value: string) => {
  const trimmedValue = value.trim()
  if (!trimmedValue) {
    return null
  }

  const match = DATE_PATTERN.exec(trimmedValue)
  if (!match) {
    return null
  }

  const [, day, month, year] = match
  const parsedDate = new Date(Number(year), Number(month) - 1, Number(day))
  if (
    parsedDate.getFullYear() !== Number(year) ||
    parsedDate.getMonth() !== Number(month) - 1 ||
    parsedDate.getDate() !== Number(day)
  ) {
    return null
  }

  return `${year}-${month}-${day}`
}
