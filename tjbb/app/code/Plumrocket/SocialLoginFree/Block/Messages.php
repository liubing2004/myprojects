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

namespace Plumrocket\SocialLoginFree\Block;

use Magento\Framework\View\Element\Message\InterpretationStrategyInterface;

class Messages extends \Magento\Framework\View\Element\Messages
{
    /**
     * @var \Plumrocket\SocialLoginFree\Helper\Data
     */
    protected $helper;

    /**
     * @var \Magento\Customer\Model\Session
     */
    protected $customerSession;

    /**
     * @var \Magento\Store\Model\Store
     */
    protected $store;

    /**
     * @var \Magento\Framework\Message\NoticeFactory
     */
    protected $noticeFactory;

    /**
     * Messages constructor.
     *
     * @param \Magento\Framework\View\Element\Template\Context $context
     * @param \Magento\Framework\Message\Factory               $messageFactory
     * @param \Magento\Framework\Message\CollectionFactory     $collectionFactory
     * @param \Magento\Framework\Message\ManagerInterface      $messageManager
     * @param InterpretationStrategyInterface                  $interpretationStrategy
     * @param \Plumrocket\SocialLoginFree\Helper\Data          $helper
     * @param \Magento\Customer\Model\Session                  $customerSession
     * @param \Magento\Store\Model\Store                       $store
     * @param \Magento\Framework\Message\NoticeFactory         $noticeFactory
     * @param array                                            $data
     */
    public function __construct(
        \Magento\Framework\View\Element\Template\Context $context,
        \Magento\Framework\Message\Factory $messageFactory,
        \Magento\Framework\Message\CollectionFactory $collectionFactory,
        \Magento\Framework\Message\ManagerInterface $messageManager,
        InterpretationStrategyInterface $interpretationStrategy,
        \Plumrocket\SocialLoginFree\Helper\Data $helper,
        \Magento\Customer\Model\Session $customerSession,
        \Magento\Store\Model\Store $store,
        \Magento\Framework\Message\NoticeFactory $noticeFactory,
        array $data = []
    ) {
        parent::__construct(
            $context,
            $messageFactory,
            $collectionFactory,
            $messageManager,
            $interpretationStrategy,
            $data
        );

        $this->helper = $helper;
        $this->customerSession = $customerSession;
        $this->store = $store;
        $this->noticeFactory = $noticeFactory;
    }

    protected function _prepareLayout()
    {
        if ($this->helper->moduleEnabled()) {
            $this->_fakeEmailMessage();
            $this->addMessages($this->messageManager->getMessages(true));
        }
        return parent::_prepareLayout();
    }

    protected function _fakeEmailMessage()
    {
        // Check email.
        $requestString = $this->_request->getRequestString();
        $module = $this->_request->getModuleName();
        $controller = $this->_request->getControllerName();
        $action = $this->_request->getActionName();

        $editUri = 'customer/account/edit';

        switch(true) {

            case (stripos($requestString, 'customer/account/logout') !== false || stripos($requestString, 'customer/section/load') !== false):
                break;

            case $moduleName = (stripos($module, 'customer') !== false) ? 'customer' : null:
            // case $moduleName = (stripos($module, 'checkout') !== false && stripos($controller, 'onepage') !== false && stripos($action, 'index') !== false) ? 'checkout' : null:

                if($this->customerSession->isLoggedIn() && $this->helper->isFakeMail()) {
                    
                    $this->messageManager->getMessages()->deleteMessageByIdentifier('fakeemail');
                    $message = __('Your account needs to be updated. The email address in your profile is invalid. Please indicate your valid email address by going to the <a href="%1">Account edit page</a>', $this->store->getUrl($editUri));

                    switch($moduleName) {
                        case 'customer':
                            if(stripos($requestString, $editUri) !== false) {
                                // Set new message and red field.
                                $message = __('Your account needs to be updated. The email address in your profile is invalid. Please indicate your valid email address.');
                            }
                            $noticeMessage = $this->noticeFactory->create(['text' => $message])->setIdentifier('fakeemail');
                            $this->messageManager->addUniqueMessages([$noticeMessage]);
                            break;

                        /*case 'checkout':
                            $this->messageManager->addUniqueMessages(Mage::getSingleton('core/message')->notice($message)->setIdentifier('fakeemail'));
                            break;*/
                    }
                    
                }
                break;
        }
    }
}
