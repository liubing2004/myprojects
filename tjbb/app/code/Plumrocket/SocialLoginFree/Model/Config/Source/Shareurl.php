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

namespace Plumrocket\SocialLoginFree\Model\Config\Source;

class Shareurl implements \Magento\Framework\Option\ArrayInterface
{
    /**
     * @var null | array[]
     */
    protected $_options = null;

    /**
     * @var \Magento\Cms\Model\Page
     */
    protected $cmsPage;

    /**
     * @var \Plumrocket\SocialLoginFree\Helper\Data
     */
    protected $dataHelper;

    /**
     * Redirectto constructor.
     *
     * @param \Magento\Cms\Model\Page $cmsPage
     */
    function __construct(
        \Magento\Cms\Model\Page $cmsPage,
        \Plumrocket\SocialLoginFree\Helper\Data $dataHelper
    ) {
        $this->cmsPage      = $cmsPage;
        $this->dataHelper   = $dataHelper;
    }

    /**
     * Options getter
     *
     * @return array
     */
    public function toOptionArray()
    {
        return $this->_getOptions();
    }

    /**
     * Get options in "key-value" format
     *
     * @return array
     */
    public function toArray()
    {
        $options = [];
        foreach ($this->_getOptions() as $option) {
            $options[ $option['value'] ] = $option['label'];
        }

        return $options;
    }

    protected function _getOptions()
    {
        if (null === $this->_options) {
            $invitationsEnabled = $this->dataHelper->moduleInvitationsEnabled();

            $options = [
                ['value' => '__custom__',  'label' => __('Redirect to Custom URL')],
                ['value' => '__invitations'. (!$invitationsEnabled? 'off' : '') .'__', 'disabled' => 'disabled', 'label' => __('Plumrocket Invitations Promo Page'. (!$invitationsEnabled? ' (Not installed)' : ''))],
                ['value' => '__none__',    'label' => __('---')],
            ];

            $items = $this->cmsPage->getCollection()->getItems();

            foreach ($items as $item) {
                if($item->getId() == 1) continue;
                $options[] = ['value' => $item->getId(), 'label' => $item->getTitle()];
            }

            $this->_options = $options;
        }

        return $this->_options;
    }
}
