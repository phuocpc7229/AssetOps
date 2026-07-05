export type PaginatedResponse<T> = {
  page: number
  page_size: number
  total_pages: number
  results: T[]
}

export type PaginationParams = {
  page?: number
  page_size?: number
}

const LOOKUP_PAGE_SIZE = 100

export const fetchAllPages = async <T, Params extends PaginationParams>(
  fetchPage: (params: Params) => Promise<PaginatedResponse<T>>,
  params: Omit<Params, 'page' | 'page_size'>,
) => {
  const results: T[] = []
  let page = 1
  let totalPages = 1

  do {
    const response = await fetchPage({
      ...params,
      page,
      page_size: LOOKUP_PAGE_SIZE,
    } as Params)

    results.push(...response.results)
    totalPages = response.total_pages
    page += 1
  } while (page <= totalPages)

  return results
}
