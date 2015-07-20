angular.module('starter')

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
  $scope.logout = function() {
    AuthService.logout();
    $state.go('login');
  };

  $scope.username = AuthService.username();

  $scope.addItem = function(data) {
    console.log("add item", data.shoplist);
    $http.get('http://52.8.58.231/mobile/additem', { params: { "userId": 2, "shopListName": data.shoplist, "store": data.store, "itemName": data.itemname } })
            .success(function(response, status, headers, config) {
		console.log("success", response["status"]);
		$state.go('main.shopitem', {}, {reload: true});
            }).error(function(response, status, headers, config) {               
                console.log("fail");
            });
   };
})

.controller('MylistCtrl', function($scope, $http, $state) {
 $scope.shouldShowDelete = false;
 $scope.shouldShowReorder = false;
 $scope.listCanSwipe = true;
 $http.get('http://52.8.58.231/mobile/shopitem', { params: { "userId": 2} })
            .success(function(response, status, headers, config) {
                console.log("success");
                $scope.items = response;
            }).error(function(response, status, headers, config) {               
                console.log("fail");
            });


$scope.delete = function(item) {
      $http.get('http://52.8.58.231/mobile/shopitem/delete', { params: { "userId": 2, "shopitemName": item.name} })
            .success(function(response, status, headers, config) {
                console.log("success!");
                $state.go('main.shopitem', {}, {reload: true});
            }).error(function(response, status, headers, config) {
                console.log("fail");
            });

    };



})


.controller('LoginCtrl', function($scope, $state, $ionicPopup, AuthService) {
  $scope.data = {};

  $scope.login = function(data) {
    AuthService.login(data.username, data.password).then(function(authenticated) {
      $state.go('main.public', {}, {reload: true});
      $scope.setCurrentUsername(data.username);
    }, function(err) {
      var alertPopup = $ionicPopup.alert({
        title: 'Login failed!',
        template: 'Please check your credentials!'
      });
    });
  };
})

.controller('ShopitemCtrl', function($scope, $state, $http, $ionicPopup, $stateParams, AuthService) {

 $scope.shouldShowDelete = false;
 $scope.shouldShowReorder = false;
 $scope.listCanSwipe = true;

 $http.get('http://52.8.58.231/mobile/shopitem', { params: { "userId": 2} })
            .success(function(response, status, headers, config) {
                console.log("successi!!!1");
                $scope.items = response;
            }).error(function(response, status, headers, config) {
                console.log("fail");
            });

$scope.shoplist_name = $stateParams["shoplist"];
$scope.delete = function(item) {
      $http.get('http://52.8.58.231/mobile/shopitem/delete', { params: { "userId": 2, "shopitemName": item.name} })
            .success(function(response, status, headers, config) {
                console.log("success!");
                $state.go('main.shopitem', {}, {reload: true});
            }).error(function(response, status, headers, config) {
                console.log("fail");
            });

    };
$scope.goDetail = function(item){
       $state.go('main.shopitem', {shoplist:"text"}, {reload: true});
    };
});

