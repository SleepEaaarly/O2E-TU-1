
function successResponse (data) {
  return data
}

export const tokenAuth = req => {
  return successResponse({
    access_token: 'test123',
    refresh_token: 'test111'
  })
}
