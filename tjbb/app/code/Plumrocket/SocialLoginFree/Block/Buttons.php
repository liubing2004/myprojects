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

class Buttons extends \Magento\Framework\View\Element\Template
{
    /**
     * @var int
     */
    protected $_countFullButtons = 6;

    /**
     * @var bool
     */
    protected $_output2js = false;

    /**
     * @var null
     */
    protected $_checkPosition = null;

    /**
     * @var \Plumrocket\SocialLoginFree\Helper\Data
     */
    protected $dataHelper;

    /**
     * Buttons constructor.
     *
     * @param \Magento\Framework\View\Element\Template\Context  $context
     * @param \Plumrocket\SocialLoginFree\Helper\Data           $dataHelper
     * @param array                                             $data
     */
    public function __construct(
        \Magento\Framework\View\Element\Template\Context $context,
        \Plumrocket\SocialLoginFree\Helper\Data $dataHelper,
        array $data = []
    ) {
        parent::__construct($context, $data);
        $this->dataHelper = $dataHelper;
    }

    /**
     * @return \Plumrocket\SocialLoginFree\Helper\Data
     */
    public function getHelper()
    {
        return $this->dataHelper;
    }

    /**
     * @param null $part
     *
     * @return array|mixed
     */
    public function getPreparedButtons($part = null)
    {
        return $this->getHelper()->getPreparedButtons($part);
    }

    public function hasButtons()
    {
        return (bool)$this->getPreparedButtons();
    }

    public function showLoginFullButtons()
    {
        $visible = $this->getPreparedButtons('visible');
        return count($visible) <= $this->_countFullButtons;
    }

    public function showRegisterFullButtons()
    {
        return $this->showFullButtons();
    }

    public function showFullButtons()
    {
        $all = $this->getPreparedButtons();
        return count($all) <= $this->_countFullButtons;
    }

    public function setFullButtonsCount($count)
    {
        if(is_numeric($count) && $count >= 0) {
            $this->_countFullButtons = $count;
        }
        return $this;
    }

    /*public function isAutocompleteDisabled()
    {
        return true;
    }*/

    public function setOutput2js($flag = true)
    {
        $this->_output2js = (bool)$flag;
    }

    public function checkPosition($position = null)
    {
        $this->_checkPosition = $position;
    }

    public function _afterToHtml($html)
    {
        if ($this->_checkPosition) {
            if (!$this->getHelper()->modulePositionEnabled($this->_checkPosition)) {
                $html = '';
            }
        }

        if ($this->_output2js && trim($html)) {
            $html = '<script type="text/javascript">'
                . 'window.psloginButtons = \'' . str_replace(["\n", 'script'], ['', "scri'+'pt"], $this->escapeJsQuote($html)) . '\';'
                . '</script>';
        }

        return parent::_afterToHtml($html);
    }
}