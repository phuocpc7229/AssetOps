import { ApiError } from './api'

export type FieldErrors<T extends string = string> = Partial<Record<T, string>>

type ErrorBody = Record<string, string | string[]>

const isErrorBody = (value: unknown): value is ErrorBody =>
  Boolean(value) && typeof value === 'object' && !Array.isArray(value)

const firstMessage = (value: string | string[] | undefined) => {
  if (Array.isArray(value)) {
    return value[0] ?? ''
  }

  return value ?? ''
}

export const parseFieldErrors = <T extends string>(error: unknown, fields: readonly T[]) => {
  const fieldErrors: FieldErrors<T> = {}

  if (!(error instanceof ApiError) || !isErrorBody(error.data)) {
    return fieldErrors
  }

  fields.forEach((field) => {
    const message = firstMessage(error.data[field])
    if (message) {
      fieldErrors[field] = message
    }
  })

  return fieldErrors
}

export const getApiErrorMessage = (error: unknown, fallback: string) => {
  if (error instanceof ApiError) {
    if (error.status >= 400 && error.status < 500) {
      return error.message
    }

    return fallback
  }

  return fallback
}
