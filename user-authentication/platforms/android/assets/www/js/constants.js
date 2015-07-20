angular.module('starter')

.constant('AUTH_EVENTS', {
  notAuthenticated: 'auth-not-authenticated',
  notAuthorized: 'auth-not-authorized'
})

.constant('SERVER', {
   URL: 'http://52.8.58.231'
})

.constant('USER_ROLES', {
  admin: 'admin_role',
  public: 'public_role'
});
