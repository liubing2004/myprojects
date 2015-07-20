// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
angular.module('starter', ['ionic', 'ngMockE2E'])
// bower install angular-mocks --save
// <script src="lib/angular-mocks/angular-mocks.js"></script>
// https://docs.angularjs.org/api/ngMockE2E
.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if(window.cordova && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
    }
    if(window.StatusBar) {
      StatusBar.styleDefault();
    }
  });
})

.config(function ($stateProvider, $urlRouterProvider, USER_ROLES) {
  $stateProvider
  .state('login', {
    url: '/login',
    templateUrl: 'templates/login.html',
    controller: 'LoginCtrl'
  })
  .state('main', {
    url: '/',
    abstract: true,
    templateUrl: 'templates/main.html'
  })
 
 .state('main.public', {
    url: 'main/public',
    cache: false,
    views: {
        'public-tab': {
          templateUrl: 'templates/public.html',
          controller: 'PublicCtrl'
        }
    }
  })

 
 .state('main.shopitem', {
    url: 'main/shopitem',
    cache: false,
    views: {
        'shopitem-tab': {
          templateUrl: 'templates/shopitem.html',
          controller: 'ShopitemCtrl'
        }
    }
  })

  .state('main.admin', {
    url: 'main/admin',
     cache: false,
    views: {
        'admin-tab': {
          templateUrl: 'templates/admin.html',
          controller:'MylistCtrl'
        }
    },
    //data: {
    //  authorizedRoles: [USER_ROLES.admin]
   // }
  });
  $urlRouterProvider.otherwise('/main/public');
})

.run(function($httpBackend){


  $httpBackend.whenGET(/templates\/\w+.*/).passThrough();
  $httpBackend.whenGET(/.*/).passThrough();
  $httpBackend.whenPOST(/.*/).passThrough();
})

.run(function ($rootScope, $state, AuthService, AUTH_EVENTS) {
  $rootScope.$on('$stateChangeStart', function (event,next, nextParams, fromState) {

    if ('data' in next && 'authorizedRoles' in next.data) {
      var authorizedRoles = next.data.authorizedRoles;
      if (!AuthService.isAuthorized(authorizedRoles)) {
        event.preventDefault();
        $state.go($state.current, {}, {reload: true});
        $rootScope.$broadcast(AUTH_EVENTS.notAuthorized);
      }
    }

    if (!AuthService.isAuthenticated()) {
      if (next.name !== 'login') {
        event.preventDefault();
        $state.go('login');
      }
    }
  });
});
