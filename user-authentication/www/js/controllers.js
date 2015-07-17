angular.module('starter')

// .controller('AppCtrl', function() {})
// .controller('LoginCtrl', function() {})
// .controller('DashCtrl', function() {});
.controller('AppCtrl', function($scope, $state, $ionicPopup, AuthService, AUTH_EVENTS) {
  $scope.username = AuthService.username();

  $scope.$on(AUTH_EVENTS.notAuthorized, function(event) {
    var alertPopup = $ionicPopup.alert({
      title: 'Unauthorized!',
      template: 'You are not allowed to access this resource.'
    });
  });

  $scope.$on(AUTH_EVENTS.notAuthenticated, function(event) {
    AuthService.logout();
    $state.go('login');
    var alertPopup = $ionicPopup.alert({
      title: 'Session Lost!',
      template: 'Sorry, You have to login again.'
    });
  });

  $scope.setCurrentUsername = function(name) {
    $scope.username = name;
  };
})

.controller('PublicCtrl', function($scope, $state, $http, AuthService) {
  $scope.username = AuthService.username();

  $scope.addItem = function(data) {
    console.log("add item", data.shoplist);
    $http.get('http://localhost:8100/mobile/additem', { params: { "userId": 2, "shopListName": data.shoplist, "store": data.store, "itemName": data.itemname } })
            .success(function(response, status, headers, config) {
		console.log("success", response["status"]);
		$state.go('main.dash', {}, {reload: true});
            }).error(function(response, status, headers, config) {               
                console.log("fail");
            });
   };
})

.controller('MylistCtrl', function($scope, $http, $state) {
 $scope.shouldShowDelete = false;
 $scope.shouldShowReorder = false;
 $scope.listCanSwipe = true;
 $http.get('http://localhost:8100/mobile/shoplist', { params: { "userId": 2} })
            .success(function(response, status, headers, config) {
                console.log("success", response["status"]);
                $scope.items = response;
            }).error(function(response, status, headers, config) {               
                console.log("fail");
            });

$scope.delete = function(item) {
      alert('Delete item: ');
    };
$scope.goDetail = function(item){
       $state.go('main.dash', {}, {reload: true});	
    };
})


.controller('ShopitemCtrl', function($scope) {
 $scope.shouldShowDelete = false;
 $scope.shouldShowReorder = false;
 $scope.listCanSwipe = true;
 $scope.items = [
    {title: "Egg"},
    {title: "Apple"},
    {title: "Oil"},
    {title: "Orange"},
    {title: "Item 5"},
  ];
$scope.delete = function(item) {
      alert('Delete item: ');
    };
$scope.goDetail = function(item){
       $state.go('main.dash', {}, {reload: true});
    };


})



.controller('LoginCtrl', function($scope, $state, $ionicPopup, AuthService) {
  $scope.data = {};

  $scope.login = function(data) {
    AuthService.login(data.username, data.password).then(function(authenticated) {
      $state.go('main.dash', {}, {reload: true});
      $scope.setCurrentUsername(data.username);
    }, function(err) {
      var alertPopup = $ionicPopup.alert({
        title: 'Login failed!',
        template: 'Please check your credentials!'
      });
    });
  };
})

.controller('DashCtrl', function($scope, $state, $http, $ionicPopup, AuthService) {
  $scope.logout = function() {
    AuthService.logout();
    $state.go('login');
  };

  $scope.performValidRequest = function() {
    //$http.get('http://localhost:8100/valid').then(
    $http.get('http://localhost/login').then(
      function(result) {
        $scope.response = result;
      });
  };

  $scope.performUnauthorizedRequest = function() {
    $http.get('http://localhost:8100/notauthorized').then(
      function(result) {
        // No result here..
      }, function(err) {
        $scope.response = err;
      });
  };

  $scope.performInvalidRequest = function() {
    $http.get('http://localhost:8100/notauthenticated').then(
      function(result) {
        // No result here..
      }, function(err) {
        $scope.response = err;
      });
  };
});
