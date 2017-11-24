<?php
/**
 * Plumrocket Inc.
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the End-user License Agreement
 * that is available through the world-wide-web at this URL:
 * http://wiki.plumrocket.net/wiki/EULA
 * If you are unable to obtain it through the world-wide-web, please
 * send an email to support@plumrocket.com so we can send you a copy immediately.
 *
 * @package     Plumrocket_SocialLoginFree
 * @copyright   Copyright (c) 2015 Plumrocket Inc. (http://www.plumrocket.com)
 * @license     http://wiki.plumrocket.net/wiki/EULA  End-user License Agreement
 */

namespace Plumrocket\SocialLoginFree\Model;

class Account extends \Magento\Framework\Model\AbstractModel
{
    const PHOTO_FILE_EXT = 'png';

    /**
     * @var null | string
     */
    protected $_type = null;

    /**
     * @var string
     */
    protected $_protocol = 'OAuth';

    /**
     * @var null | int
     */
    protected $_websiteId = null;

    /**
     * @var null | string
     */
    protected $_redirectUri = null;

    /**
     * @var array
     */
    protected $_userData = [];

    /**
     * @var int
     */
    protected $_passwordLength = 6;

    /**
     * @var null | string
     */
    protected $_photoDir = null;

    /**
     * @var int
     */
    protected $_photoSize = 150;

    /**
     * @var null | string | int
     */
    protected $_applicationId = null;

    /**
     * @var null | string | int
     */
    protected $_secret = null;

    /**
     * @var string
     */
    protected $_responseType = 'code';

    /**
     * @var array
     */
    protected $_dob = [];

    /**
     * @var array
     */
    protected $_gender = ['male', 'female'];

    /**
     * @var \Plumrocket\SocialLoginFree\Helper\Data
     */
    protected $_helper;

    /**
     * @var \Magento\Store\Model\StoreManager
     */
    protected $storeManager;

    /**
     * @var \Magento\Store\Model\Store
     */
    protected $store;

    /**
     * @var \Magento\Framework\Filesystem
     */
    protected $filesystem;

    /**
     * @var \Magento\Framework\Encryption\Encryptor
     */
    protected $encryptor;

    /**
     * @var \Magento\Customer\Model\Customer
     */
    protected $customer;

    /**
     * @var \Magento\Newsletter\Model\SubscriberFactory
     */
    protected $subscriberFactory;

    /**
     * @var \Magento\Eav\Model\Config
     */
    protected $eavConfig;

    /**
     * @var \Magento\Customer\Model\Attribute
     */
    protected $attribute;

    /**
     * @var \Magento\Framework\Math\Random
     */
    protected $random;

    /**
     * @var \Magento\Framework\Filesystem\Io\File
     */
    protected $ioFile;

    /**
     * @var \Magento\Framework\ImageFactory
     */
    protected $imageFactory;

    /**
     * Account constructor.
     *
     * @param \Magento\Framework\Model\Context                             $context
     * @param \Magento\Framework\Registry                                  $registry
     * @param \Plumrocket\SocialLoginFree\Helper\Data                      $dataHelper
     * @param \Magento\Store\Model\StoreManager                            $storeManager
     * @param \Magento\Store\Model\Store                                   $store
     * @param \Magento\Framework\Filesystem                                $filesystem
     * @param \Magento\Framework\Encryption\Encryptor                      $encryptor
     * @param \Magento\Customer\Model\Customer                             $customer
     * @param \Magento\Newsletter\Model\SubscriberFactory                  $subscriberFactory
     * @param \Magento\Eav\Model\Config                                    $eavConfig
     * @param \Magento\Customer\Model\Attribute                            $attribute
     * @param \Magento\Framework\Math\Random                               $random
     * @param \Magento\Framework\Filesystem\Io\File                        $ioFile
     * @param \Magento\Framework\ImageFactory                              $imageFactory
     * @param \Magento\Framework\Model\ResourceModel\AbstractResource|null $resource
     * @param \Magento\Framework\Data\Collection\AbstractDb|null           $resourceCollection
     * @param array                                                        $data
     */
    public function __construct(
        \Magento\Framework\Model\Context $context,
        \Magento\Framework\Registry $registry,
        \Plumrocket\SocialLoginFree\Helper\Data $dataHelper,
        \Magento\Store\Model\StoreManager $storeManager,
        \Magento\Store\Model\Store $store,
        \Magento\Framework\Filesystem $filesystem,
        \Magento\Framework\Encryption\Encryptor $encryptor,
        \Magento\Customer\Model\Customer $customer,
        \Magento\Newsletter\Model\SubscriberFactory $subscriberFactory,
        \Magento\Eav\Model\Config $eavConfig,
        \Magento\Customer\Model\Attribute $attribute,
        \Magento\Framework\Math\Random $random,
        \Magento\Framework\Filesystem\Io\File $ioFile,
        \Magento\Framework\ImageFactory $imageFactory,

        \Magento\Framework\Model\ResourceModel\AbstractResource $resource = null,
        \Magento\Framework\Data\Collection\AbstractDb $resourceCollection = null,
        array $data = []
    ) {
        $this->_helper = $dataHelper;
        $this->storeManager = $storeManager;
        $this->store = $store;
        $this->filesystem = $filesystem;
        $this->encryptor = $encryptor;
        $this->customer = $customer;
        $this->subscriberFactory = $subscriberFactory;
        $this->eavConfig = $eavConfig;
        $this->attribute = $attribute;
        $this->random = $random;
        $this->ioFile = $ioFile;
        $this->imageFactory = $imageFactory;
        parent::__construct($context, $registry, $resource, $resourceCollection, $data);
    }

    public function _construct()
    {
        // if (Mage::getSingleton('plumbase/observer')->customer() == Mage::getSingleton('plumbase/product')->currentCustomer()) {
            $this->_init('Plumrocket\SocialLoginFree\Model\ResourceModel\Account');
            $this->_websiteId = $this->storeManager->getWebsite()->getId();
            $this->_redirectUri = $this->_helper->getCallbackURL($this->_type);
            $this->_photoDir = $this->filesystem->getDirectoryRead(\Magento\Framework\App\Filesystem\DirectoryList::MEDIA)->getAbsolutePath('pslogin'. DIRECTORY_SEPARATOR .'photo');
            $this->_applicationId = trim($this->_helper->getConfig($this->_helper->getConfigSectionId() .'/'. $this->_type .'/application_id'));

            $this->_secret = trim($this->encryptor->decrypt($this->_helper->getConfig($this->_helper->getConfigSectionId() .'/'. $this->_type .'/secret')));
        // }
    }

    public function enabled()
    {
        return (bool)$this->_helper->getConfig($this->_helper->getConfigSectionId() .'/'. $this->_type .'/enable');
    }

    public function setCustomerIdByUserId($customerId)
    {
        $data = [
            'type' => $this->_type,
            'user_id' => $this->getUserData('user_id'),
            'customer_id' => $customerId
        ];

        $this->addData($data)->save();
        return $this;
    }

    public function getCustomerIdByUserId()
    {
        $customerId = $this->_getCustomerIdByUserId();
        if (!$customerId && $this->_helper->isGlobalScope()) {
            $customerId = $this->_getCustomerIdByUserId(true);
        }

        return $customerId;
    }

    protected function _getCustomerIdByUserId($useGlobalScope = false)
    {
        $customerId = 0;

        if ($this->getUserData('user_id')) {
            $collection = $this->getCollection()
                ->join(['ce' => 'customer_entity'], 'ce.entity_id = main_table.customer_id', null)
                ->addFieldToFilter('main_table.type', $this->_type)
                ->addFieldToFilter('main_table.user_id', $this->getUserData('user_id'))
                ->setPageSize(1);

            if ($useGlobalScope == false) {
                $collection->addFieldToFilter('ce.website_id', $this->_websiteId);
            }

            $customerId = $collection->getFirstItem()->getData('customer_id');
        }

        return $customerId;
    }

    public function getCustomerIdByEmail()
    {
        $customerId = $this->_getCustomerIdByEmail();
        if (!$customerId && $this->_helper->isGlobalScope()) {
            $customerId = $this->_getCustomerIdByEmail(true);
        }
        return $customerId;
    }

    protected function _getCustomerIdByEmail($useGlobalScope = false)
    {
        $customerId = 0;

        if (is_string($this->getUserData('email'))) {
            $collection = $this->customer->getCollection()
                ->addFieldToFilter('email', $this->getUserData('email'))
                ->setPageSize(1);

            if ($useGlobalScope == false) {
                $collection->addFieldToFilter('website_id', $this->_websiteId);
            }

            $customerId = $collection->getFirstItem()->getId();
        }

        return $customerId;
    }

    public function registrationCustomer()
    {
        $customerId = 0;
        $errors = [];
        $customer = $this->customer->setId(null);

        try{
            $customer->setData($this->getUserData())
                ->setConfirmation($this->getUserData('password'))
                ->setPasswordConfirmation($this->getUserData('password'))
                ->setData('is_active', 1)
                ->getGroupId();

            $errors = $this->_validateErrors($customer);

            // If email is not valid, always error.
            $correctEmail = \Zend_Validate::is($this->getUserData('email'), 'EmailAddress');

            if ( (empty($errors) || $this->_helper->validateIgnore()) && $correctEmail) {
                $customerId = $customer->save()->getId();

                if (! $this->_helper->isFakeMail($this->getUserData('email'))
                    && $this->_helper->getConfig($this->_helper->getConfigSectionId() . '/general/enable_subscription')
                ) {
                    $this->subscriberFactory->create()->subscribeCustomerById($customerId);
                }

                // Set email confirmation;
                $customer->setConfirmation(null)->save();
                /*$customer->setConfirmation(null)
                    ->getResource()->saveAttribute($customer, 'confirmation');*/

            }
        } catch (\Exception $e) {
            $errors[] = $e->getMessage();
        }

        $this->setCustomer($customer);
        $this->setErrors($errors);

        return $customerId;
    }

    protected function _validateErrors($customer)
    {
        $errors = [];

        // Date of birth.
        $entityType = $this->eavConfig->getEntityType('customer');
        $attribute = $this->attribute->loadByCode($entityType, 'dob');

        if ($attribute->getIsRequired() && $this->getUserData('dob')
            && !\Zend_Validate::is($this->getUserData('dob'), 'Date')
        ) {
            $errors[] = __('The Date of Birth is not correct.');
        }

        if (true !== ($customerErrors = $customer->validate())) {
            $errors = array_merge($customerErrors, $errors);
        }

        return $errors;
    }

    public function getResponseType()
    {
        return $this->_responseType;
    }

    public function setUserData($key, $value = null)
    {
        if (is_array($key)) {
            $this->_userData = array_merge($this->_userData, $key);
        }else{
            $this->_userData[$key] = $value;
        }
        return $this;
    }

    public function getUserData($key = null)
    {
        if ($key !== null) {
            return isset($this->_userData[$key]) ? $this->_userData[$key] : null;
        }
        return $this->_userData;
    }

    protected function _prepareData($data)
    {
        $_data = [];
        foreach ($this->_fields as $customerField => $userField) {
            $_data[$customerField] = ($userField && isset($data[$userField])) ? $data[$userField] : null;
        }

        $firstname = '-';
        $lastname = '-';

        // Generate email.
        if (empty($_data['email']) && $this->_helper->validateIgnore()) {
            $_data['email'] = $this->_getRandomEmail();
        } elseif (!empty($_data['email'])) {
            $email = trim(strstr($_data['email'], '@', true));
            if ($email) {
                $email = preg_split('#[.\-]+#ui', $email, 2);

                $firstname = $lastname = ucfirst($email[0]);
                if (! empty($email[1])) {
                    $lastname = ucfirst($email[1]);
                }
            }
        }

        $_data['firstname'] = $_data['firstname'] ?: $firstname;
        $_data['lastname'] = $_data['lastname'] ?: $lastname;

        // Prepare date of birth.
        if (!empty($_data['dob'])) {
            $_data['dob'] = call_user_func_array([$this, '_prepareDob'], array_merge([$_data['dob']], $this->_dob));
        } else {
            $_data['dob'] = '0000-00-00';
        }

        // Convert gender.
        if (!empty($_data['gender'])) {
            $genderAttribute = $this->eavConfig->getAttribute('customer', 'gender');
            if ($genderAttribute && $options = $genderAttribute->getSource()->getAllOptions(false)) {
                switch($_data['gender']) {
                    case $this->_gender[0]: $_data['gender'] = $options[0]['value']; break;
                    case $this->_gender[1]: $_data['gender'] = $options[1]['value']; break;
                    default: $_data['gender'] = 0;
                }
            } else {
                $_data['gender'] = 0;
            }
        } else {
            $_data['gender'] = 0;
        }

        // Tax/Vat number.
        $_data['taxvat'] = '0';

        // Set password.
        $_data['password'] = $this->_getRandomPassword();

        return $_data;
    }

    protected function _prepareDob($date, $p1 = 'month', $p2 = 'day', $p3 = 'year', $separator = '/')
    {
        $date = explode($separator, $date);

        $result = [
            'year' => '0000',
            'month' => '00',
            'day' => '00'
        ];

        $result[$p1] = $date[0];
        if (isset($date[1])) $result[$p2] = $date[1];
        if (isset($date[2])) $result[$p3] = $date[2];

        return implode('-', array_values($result));
    }

    protected function _getRandomEmail()
    {
        $len = 10;
        $chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
        $domain = parse_url($this->store->getBaseUrl(), PHP_URL_HOST);
        $address = \Plumrocket\SocialLoginFree\Helper\Data::FAKE_EMAIL_PREFIX . $this->random->getRandomString($len, $chars) .'@'. $domain;
        return $address;
    }

    protected function _getRandomPassword()
    {
        $len = $this->_passwordLength;
        $chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
        return $this->random->getRandomString($len, $chars);
    }

    public function setCustomerPhoto($customerId)
    {
        $upload = false;

        $fileUrl = $this->getUserData('photo');
        if (empty($fileUrl) || !is_numeric($customerId) || $customerId < 1) {
            return;
        }

        $tmpPath = $this->_photoDir . DIRECTORY_SEPARATOR . $customerId .'.tmp';

        try {
            $this->ioFile->mkdir($this->_photoDir);
            if ($file = $this->_loadFile($fileUrl)) {
                if (file_put_contents($tmpPath, $file) > 0) {

                    $image = $this->imageFactory->create(['fileName' => $tmpPath]);
                    $image->resize($this->_photoSize);

                    $fileName = $customerId .'.'. self::PHOTO_FILE_EXT;
                    $image->save(null, $fileName);

                    $upload = true;
                }
            }
        } catch (\Exception $e) {}

        if ($this->ioFile->fileExists($tmpPath)) {
            $this->ioFile->rm($tmpPath);
        }

        return $upload;
    }

    protected function _loadFile($url, $count = 1) {

        if ($count > 5) {
            return false;
        }

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_HEADER, true);
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        $data = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

        curl_close($ch);

        if (!$data) {
            return false;
        }

        $dataArray = explode("\r\n\r\n", $data, 2);

        if (count($dataArray) != 2) {
            return false;
        }

        list($header, $body) = $dataArray;
        if ($httpCode == 301 || $httpCode == 302) {
            $matches = [];
            preg_match('/Location:(.*?)\n/', $header, $matches);

            if (isset($matches[1])) {
                return $this->_loadFile(trim($matches[1]), $count++);
            }
        } else {
            return $body;
        }
    }

    public function postToMail()
    {
        if (!$this->_helper->isFakeMail( $this->getUserData('email') )) {
            $storeId = $this->storeManager->getStore()->getId();
            $this->customer->sendNewAccountEmail('registered', '', $storeId);
        }

        return true;
    }

    public function getButton()
    {
        // Href.
        $uri = null;

        // if (Mage::getSingleton('plumbase/observer')->customer() == Mage::getSingleton('plumbase/product')->currentCustomer()) {
            if ($this->getProtocol() == 'OAuth' && (empty($this->_applicationId) || empty($this->_secret))) {
                $uri = null;
            }else{
                $uri = $this->store->getUrl('pslogin/account/douse', ['type' => $this->_type, 'refresh' => time()]);
            }
        // }

        // Images.
        $image = [];
        $media = $this->store->getBaseUrl(\Magento\Framework\UrlInterface::URL_TYPE_MEDIA) .'pslogin/';

        // ..icon
        $iconBtn = $this->_helper->getConfig($this->_helper->getConfigSectionId() .'/'. $this->_type .'/icon_btn');
        $image['icon'] = $iconBtn? $media . $iconBtn : null;

        // ..login
        $loginBtn = $this->_helper->getConfig($this->_helper->getConfigSectionId() .'/'. $this->_type .'/login_btn');
        $image['login'] = $loginBtn? $media . $loginBtn : null;

        // ..register
        $registerBtn = $this->_helper->getConfig($this->_helper->getConfigSectionId() .'/'. $this->_type .'/register_btn');
        $image['register'] = $registerBtn? $media . $registerBtn : null;

        return [
            'href' => $uri,
            'type' => $this->_type,
            'image' => $image,
            'login_text' => $this->_helper->getConfig($this->_helper->getConfigSectionId() .'/'. $this->_type .'/login_btn_text'),
            'register_text' => $this->_helper->getConfig($this->_helper->getConfigSectionId() .'/'. $this->_type .'/register_btn_text'),
            'popup_width' => $this->_popupSize[0],
            'popup_height' => $this->_popupSize[1],
        ];
    }

    public function getProviderLink()
    {
        if (empty($this->_applicationId) || empty($this->_secret)) {
            $uri = null;
        }elseif (is_array($this->_buttonLinkParams)) {
            $uri = $this->_url .'?'. urldecode(http_build_query($this->_buttonLinkParams));
        }else{
            $uri = $this->_buttonLinkParams;
        }

        return $uri;
    }

    public function getProvider()
    {
        return $this->_type;
    }

    public function getProtocol()
    {
        return $this->_protocol;
    }

    public function _setLog($data, $append = false)
    {
        return;
    }

    protected function _call($url, $params = [], $method = 'GET', $curlResource = null)
    {
        $result = null;
        $paramsStr = is_array($params)? urlencode(http_build_query($params)) : urlencode($params);
        if ($paramsStr) {
            $url .= '?'. urldecode($paramsStr);
        }

        $curl = is_resource($curlResource)? $curlResource : curl_init();

        if ($method == 'POST') {
            // POST.
            curl_setopt($curl, CURLOPT_URL, $url);
            curl_setopt($curl, CURLOPT_POST, 1);
            curl_setopt($curl, CURLOPT_POSTFIELDS, $paramsStr);
        }else{
            // GET.
            curl_setopt($curl, CURLOPT_URL, $url);
        }

        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

        // if (Mage::getSingleton('plumbase/observer')->customer() == Mage::getSingleton('plumbase/product')->currentCustomer()) {
            $result = curl_exec($curl);
        // }
        curl_close($curl);

        return $result;
    }
}