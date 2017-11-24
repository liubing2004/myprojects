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

class Template extends \Magento\Framework\View\Element\Template
{
    /**
     * @var \Plumrocket\SocialLoginFree\Helper\Data
     */
    protected $dataHelper;

    /**
     * @param \Magento\Framework\View\Element\Template\Context $context
     * @param \Plumrocket\SocialLoginFree\Helper\Data          $dataHelper
     * @param array                                            $data
     */
    public function __construct(
        \Magento\Framework\View\Element\Template\Context $context,
        \Plumrocket\SocialLoginFree\Helper\Data $dataHelper,
        array $data = []
    ) {
        $this->dataHelper = $dataHelper;
        parent::__construct($context, $data);
    }

    /**
     * Get data helper
     *
     * @return \Plumrocket\SocialLoginFree\Helper\Data
     */
    public function getDataHelper()
    {
        return $this->dataHelper;
    }

    /**
     * {@inheritdoc}
     */
    protected function _toHtml()
    {
        if (! $this->dataHelper->moduleEnabled()) {
            return '';
        }

        return parent::_toHtml();
    }
}
